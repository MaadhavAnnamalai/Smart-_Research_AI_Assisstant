# main.py
import os
import uuid
from datetime import datetime
from typing import List, Optional
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi import WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader
from langchain.docstore.document import Document
from dotenv import load_dotenv
from pydantic import BaseModel
from services.enhanced_conversational_agent import EnhancedConversationalAgent
from services.structured_research_agent import StructuredResearchAgent, ResearchReport
from services.live_data_service import LiveDataService
from services.billing_service_fixed import BillingService

# ----------------------------
# 0️⃣ Load environment
# ----------------------------
load_dotenv()  # Load variables from .env
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if OPENAI_API_KEY:
    print("[SUCCESS] OPENAI_API_KEY loaded successfully")
    import openai
    openai.api_key = OPENAI_API_KEY
else:
    print("[WARNING] OPENAI_API_KEY not found, switching to MOCK mode")

# ----------------------------
# 1️⃣ Request/Response Models
# ----------------------------
class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None
    user_id: str = "default"

class ChatResponse(BaseModel):
    response: dict
    session_id: str
    message_id: str
    timestamp: str

# ----------------------------
# 2️⃣ Services Initialization
# ----------------------------
# Initialize the conversational agent
try:
    conversational_agent = EnhancedConversationalAgent()
    print("[SUCCESS] Enhanced Conversational Research Agent initialized successfully")
except Exception as e:
    print(f"[ERROR] Failed to initialize Enhanced Conversational Research Agent: {e}")
    conversational_agent = None

# Initialize live data service
try:
    live_data_service = LiveDataService()
    print("[SUCCESS] Live Data Service initialized successfully")
except Exception as e:
    print(f"[ERROR] Failed to initialize Live Data Service: {e}")
    live_data_service = None

# Initialize billing service
try:
    billing_service = BillingService()
    print("[SUCCESS] Billing Service initialized successfully")
except Exception as e:
    print(f"[ERROR] Failed to initialize Billing Service: {e}")
    billing_service = None

# Initialize structured research agent
try:
    research_agent = StructuredResearchAgent()
    print("[SUCCESS] Structured Research Agent initialized successfully")
except Exception as e:
    print(f"[ERROR] Failed to initialize Structured Research Agent: {e}")
    research_agent = None

# ----------------------------
# 3️⃣ FastAPI app
# ----------------------------
app = FastAPI(title="Smart Research Assistant")


# Configure CORS based on environment
allowed_origins = [
    "http://localhost:3000",  # React dev server
    "http://localhost:8501",  # Streamlit dev server
    "http://127.0.0.1:3000",
    "http://127.0.0.1:8501",
]

# In development, allow all origins for easier testing
if os.getenv("ENVIRONMENT", "development") == "development":
    allowed_origins = ["*"]
    print("⚠️ [DEVELOPMENT] CORS allows all origins")
else:
    print(f"🔒 [PRODUCTION] CORS restricted to: {allowed_origins}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"]
)

# ----------------------------
# 4️⃣ API Endpoints
# ----------------------------

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "agent_available": conversational_agent is not None,
        "research_agent_available": research_agent is not None,
        "services": {
            "conversational_agent": conversational_agent is not None,
            "research_agent": research_agent is not None,
            "live_data_service": live_data_service is not None,
            "billing_service": billing_service is not None
        }
    }

@app.post("/api/chat", response_model=ChatResponse)
async def chat_with_agent(request: ChatRequest):
    """Chat with the research agent"""
    if not conversational_agent:
        raise HTTPException(status_code=503, detail="Conversational agent not available")
    
    try:
        # Generate session ID if not provided
        session_id = request.session_id or str(uuid.uuid4())
        
        # Process chat message
        result = await conversational_agent.chat(
            message=request.message,
            session_id=session_id,
            user_id=request.user_id
        )
        
        # Track billing: bill per question
        if billing_service:
            await billing_service.track_usage(
                user_id=request.user_id,
                event_type="question",
                credits_used=billing_service.get_credit_cost("question"),
                description=f"Question: {request.message[:50]}..."
            )
        
        return ChatResponse(**result)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/chat/{session_id}/history")
async def get_chat_history(session_id: str):
    """Get chat history for a session"""
    if not conversational_agent:
        raise HTTPException(status_code=503, detail="Conversational agent not available")
    
    try:
        history = conversational_agent.get_conversation_history(session_id)
        return {"session_id": session_id, "history": history}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/upload")
async def upload_files(files: List[UploadFile] = File(...), user_id: str = "default", file_type: str = "general"):
    """Upload and process documents"""
    if not conversational_agent:
        raise HTTPException(status_code=503, detail="Conversational agent not available")
    
    try:
        processed_files = []
        
        for file in files:
            # Save file temporarily
            file_path = f"./uploads/{file.filename}"
            os.makedirs("./uploads", exist_ok=True)
            
            with open(file_path, "wb") as buffer:
                content = await file.read()
                buffer.write(content)
            
            # Process based on file type
            if file.filename.endswith('.pdf'):
                loader = PyPDFLoader(file_path)
                documents = loader.load()
            elif file.filename.endswith('.docx'):
                loader = Docx2txtLoader(file_path)
                documents = loader.load()
            else:
                # Assume text file
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                documents = [Document(page_content=content, metadata={"source": file.filename})]
            
            # Add to conversational agent
            success = await conversational_agent.add_documents(documents, file_type)
            
            if success:
                processed_files.append({
                    "filename": file.filename,
                    "file_type": file.filename.split('.')[-1],
                    "size": len(content),
                    "processed_at": datetime.utcnow().isoformat()
                })
                
                # Track billing
                if billing_service:
                    await billing_service.track_usage(
                        user_id=user_id,
                        event_type="file_upload",
                        credits_used=1,
                        description=f"Uploaded file: {file.filename}"
                    )
            
            # Clean up temp file
            os.remove(file_path)
        
        return {
            "message": f"{len(processed_files)} files processed successfully",
            "files": processed_files
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/agent/stats")
async def get_agent_stats():
    """Get agent statistics"""
    if not conversational_agent:
        raise HTTPException(status_code=503, detail="Conversational agent not available")
    
    try:
        stats = conversational_agent.get_agent_stats()
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/live")
async def get_live_data():
    """Get live data updates"""
    if not live_data_service:
        raise HTTPException(status_code=503, detail="Live data service not available")
    
    try:
        live_data = await live_data_service.get_live_data()
        
        # Add to conversational agent cache
        if conversational_agent:
            await conversational_agent.add_live_data(live_data.get("items", []))
        # Bill for live data refresh
        if billing_service:
            await billing_service.track_usage(
                user_id="default",
                event_type="live_data",
                credits_used=billing_service.get_credit_cost("live_data"),
                description="Live data refresh"
            )
        
        return live_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/dashboard/{user_id}")
async def get_dashboard_data(user_id: str):
    """Get dashboard data for a user"""
    try:
        # Get usage stats from billing service
        usage_stats = {}
        if billing_service:
            usage_stats = await billing_service.get_usage_stats(user_id)
        
        # Get agent stats
        agent_stats = {}
        if conversational_agent:
            agent_stats = conversational_agent.get_agent_stats()
        
        return {
            "user_id": user_id,
            "usage_stats": usage_stats,
            "agent_stats": agent_stats,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ===================================
# NEW STRUCTURED RESEARCH ENDPOINTS
# ===================================

@app.post("/api/research", response_model=ResearchReport)
async def generate_research_report(request: ChatRequest):
    """Generate a structured research report with proper citations"""
    if not research_agent:
        raise HTTPException(status_code=503, detail="Research agent not available")
    
    try:
        # Generate structured research report
        report = await research_agent.generate_research_report(
            query=request.message,
            user_id=request.user_id
        )
        
        # Track billing: bill per report
        if billing_service:
            await billing_service.track_usage(
                user_id=request.user_id,
                event_type="report",
                credits_used=billing_service.get_credit_cost("report"),
                description=f"Research report: {request.message[:50]}..."
            )
        
        return report
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/research/upload")
async def upload_research_documents(files: List[UploadFile] = File(...), user_id: str = "default", source_type: str = "document"):
    """Upload documents specifically for research analysis"""
    if not research_agent:
        raise HTTPException(status_code=503, detail="Research agent not available")
    
    try:
        processed_files = []
        
        for file in files:
            # Save file temporarily
            file_path = f"./uploads/{file.filename}"
            os.makedirs("./uploads", exist_ok=True)
            
            with open(file_path, "wb") as buffer:
                content = await file.read()
                buffer.write(content)
            
            # Process based on file type
            if file.filename.endswith('.pdf'):
                loader = PyPDFLoader(file_path)
                documents = loader.load()
            elif file.filename.endswith('.docx'):
                loader = Docx2txtLoader(file_path)
                documents = loader.load()
            else:
                # Assume text file
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                documents = [Document(page_content=content, metadata={"source": file.filename})]
            
            # Add to research agent
            success = await research_agent.add_documents(documents, source_type)
            
            # Also add to conversational agent for compatibility
            if conversational_agent:
                await conversational_agent.add_documents(documents, source_type)
            
            if success:
                processed_files.append({
                    "filename": file.filename,
                    "file_type": file.filename.split('.')[-1],
                    "size": len(content),
                    "processed_at": datetime.utcnow().isoformat(),
                    "added_to_research_db": True
                })
                
                # Track billing
                if billing_service:
                    await billing_service.track_usage(
                        user_id=user_id,
                        event_type="research_file_upload",
                        credits_used=1,
                        description=f"Research file: {file.filename}"
                    )
            
            # Clean up temp file
            os.remove(file_path)
        
        return {
            "message": f"{len(processed_files)} files added to research database",
            "files": processed_files
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/research/stats")
async def get_research_stats():
    """Get research agent statistics"""
    if not research_agent:
        raise HTTPException(status_code=503, detail="Research agent not available")
    
    try:
        stats = research_agent.get_agent_stats()
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class IngestRequest(BaseModel):
    title: str
    summary: str
    link: Optional[str] = None
    source: Optional[str] = "Mock Live Source"
    category: Optional[str] = "Updates"

@app.post("/api/research/live")
async def update_research_live_data():
    """Update research agent with latest live data"""
    if not research_agent or not live_data_service:
        raise HTTPException(status_code=503, detail="Required services not available")
    
    try:
        # Get latest live data
        live_data = await live_data_service.get_live_data()
        
        # Add to research agent
        await research_agent.add_live_data(live_data.get("items", []))
        
        return {
            "message": "Research database updated with latest live data",
            "items_added": len(live_data.get("items", [])),
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/live/ingest")
async def ingest_live_item(request: IngestRequest, user_id: str = "default"):
    """Incrementally ingest a single live item and refresh agents."""
    if not live_data_service:
        raise HTTPException(status_code=503, detail="Live data service not available")

    try:
        # Ingest new live item
        new_item = await live_data_service.ingest_mock_update(
            title=request.title,
            summary=request.summary,
            link=request.link or "",
            source=request.source or "Mock Live Source",
            category=request.category or "Updates"
        )
        # Update agents with this item
        if research_agent:
            await research_agent.add_live_data([new_item])
        if conversational_agent:
            await conversational_agent.add_live_data([new_item])

        # Bill for live data refresh
        if billing_service:
            await billing_service.track_usage(
                user_id=user_id,
                event_type="live_data",
                credits_used=billing_service.get_credit_cost("live_data"),
                description="Incremental live item ingested"
            )

        return {
            "message": "Live item ingested",
            "item": new_item,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"message": "Smart Research Assistant is running"}

# ----------------------------
# 4.1️⃣ Realtime billing WebSocket
# ----------------------------

@app.websocket("/ws/billing/{user_id}")
async def billing_ws(websocket: WebSocket, user_id: str):
    await websocket.accept()
    queue = None
    try:
        if not billing_service:
            await websocket.send_json({"type": "error", "message": "Billing service unavailable"})
            await websocket.close(code=1011)
            return

        # Subscribe and send initial snapshot
        queue = await billing_service.subscribe(user_id)
        snapshot = await billing_service.get_usage_stats(user_id)
        await websocket.send_json({"type": "snapshot", "usage_stats": snapshot})

        while True:
            # Forward realtime billing events
            message = await queue.get()
            await websocket.send_json(message)
    except WebSocketDisconnect:
        pass
    except Exception as e:
        try:
            await websocket.send_json({"type": "error", "message": str(e)})
        except Exception:
            pass
    finally:
        if queue is not None and billing_service:
            billing_service.unsubscribe(user_id, queue)

# ----------------------------
# 5️⃣ Run server
# ----------------------------
if __name__ == "__main__":
    import sys
    
    # Get configuration from environment variables
    host = os.getenv("HOST", "127.0.0.1")  # Default to localhost for security
    port = int(os.getenv("PORT", "8000"))
    debug = os.getenv("DEBUG", "False").lower() == "true"
    
    # In production, use 0.0.0.0 only if explicitly set
    if "--production" in sys.argv or os.getenv("ENVIRONMENT") == "production":
        host = "0.0.0.0"
        print("🚀 [PRODUCTION MODE] Running on all interfaces (0.0.0.0)")
    else:
        print(f"🔧 [DEVELOPMENT MODE] Running on {host}:{port}")
        print("   Use --production flag or ENVIRONMENT=production for public access")
    
    # Run with proper configuration
    if debug:
        # In debug mode, run without reload to avoid import issues
        uvicorn.run("main:app", host=host, port=port, reload=False, log_level="info")
    else:
        uvicorn.run(app, host=host, port=port)
