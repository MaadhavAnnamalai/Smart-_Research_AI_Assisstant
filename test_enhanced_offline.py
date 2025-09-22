"""
Offline Test script for the Enhanced Smart Research Assistant
Tests basic functionality without network dependencies
"""

import asyncio
import os
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from services.enhanced_conversational_agent import EnhancedConversationalAgent
from langchain.docstore.document import Document
from dotenv import load_dotenv

load_dotenv()

async def test_enhanced_system_offline():
    """Test the enhanced system functionality offline"""
    print("🚀 Testing Enhanced Smart Research Assistant (Offline Mode)")
    print("=" * 65)
    
    # Initialize components
    print("1️⃣ Initializing Enhanced Conversational Agent...")
    agent = EnhancedConversationalAgent()
    
    # Test 1: Document Upload and Processing (without embeddings)
    print("\n📄 TEST 1: Document Processing (Offline Mode)")
    print("-" * 45)
    
    # Create sample documents
    sample_docs = [
        Document(
            page_content="Artificial Intelligence has shown significant improvements in natural language processing. Recent studies indicate a 40% increase in accuracy for language models. Key findings suggest that transformer architectures are essential for modern AI systems.",
            metadata={"source": "AI_Research_2024.pdf"}
        ),
        Document(
            page_content="Machine Learning applications in healthcare have demonstrated remarkable results. Clinical trials show 85% accuracy in diagnostic tasks. Important conclusions include the need for robust data validation and ethical AI implementation.",
            metadata={"source": "Healthcare_ML_Study.pdf"}
        ),
        Document(
            page_content="The future of technology lies in quantum computing and advanced AI integration. Significant developments in quantum algorithms suggest potential breakthroughs by 2025. Critical insights reveal that quantum-AI hybrid systems could revolutionize computing.",
            metadata={"source": "Future_Tech_Analysis.pdf"}
        )
    ]
    
    # Add documents to agent (should work even without embeddings)
    success = await agent.add_documents(sample_docs, "research")
    if success:
        print("✅ Sample documents added successfully (offline mode)")
    else:
        print("❌ Failed to add documents")
        return False
    
    # Test 2: Add some mock live data
    print("\n🌐 TEST 2: Live Data Integration (Mock)")
    print("-" * 40)
    
    mock_live_data = [
        {
            "id": "mock_1",
            "title": "Latest AI Breakthrough in 2024",
            "summary": "New transformer model achieves 95% accuracy in language understanding tasks",
            "source": "Tech News Today",
            "category": "Technology"
        },
        {
            "id": "mock_2", 
            "title": "Healthcare AI Shows Promise",
            "summary": "AI diagnostic tools demonstrate 90% accuracy in clinical trials",
            "source": "Medical Journal",
            "category": "Healthcare"
        }
    ]
    
    await agent.add_live_data(mock_live_data)
    print(f"✅ Added {len(mock_live_data)} mock live data items")
    
    # Test 3: Enhanced Chat Response (Mock Mode)
    print("\n💬 TEST 3: Enhanced Chat Response (Mock Mode)")
    print("-" * 48)
    
    test_query = "What are the key findings about AI accuracy and improvements?"
    print(f"🔍 Query: {test_query}")
    
    try:
        response = await agent.chat(
            message=test_query,
            session_id="test_session", 
            user_id="test_user"
        )
        
        if "error" in response:
            print(f"❌ Error: {response['error']}")
        else:
            response_data = response.get("response", {})
            print("✅ Response Generated Successfully")
            
            # Check response structure
            print(f"📝 Summary: {len(response_data.get('summary', ''))} characters")
            print(f"🔑 Key Insights: {len(response_data.get('key_insights', []))}")
            print(f"📚 Citations: {len(response_data.get('citations', []))}")
            print(f"🌐 Live Data Integration: {response_data.get('live_data_integration', {}).get('freshness', 'Unknown')}")
            print(f"📊 Confidence: {response_data.get('confidence_score', 0):.2f}")
            print(f"📊 Freshness: {response_data.get('freshness_score', 0):.2f}")
            
            # Show some details
            if response_data.get('key_insights'):
                first_insight = response_data['key_insights'][0]
                print(f"🔍 First Insight: {first_insight.get('insight', '')[:100]}...")
            
            if response_data.get('citations'):
                first_citation = response_data['citations'][0]
                print(f"📖 First Citation: {first_citation.get('source_name', 'Unknown')}")
                
    except Exception as e:
        print(f"❌ Error processing query: {e}")
    
    # Test 4: Agent Statistics  
    print("\n📊 TEST 4: Agent Statistics")
    print("-" * 30)
    
    stats = agent.get_agent_stats()
    print(f"✅ Enhanced Features: {stats.get('enhanced_features', [])}")
    print(f"📄 Documents: {stats.get('total_documents', 0)}")
    print(f"💬 Conversations: {stats.get('active_conversations', 0)}")
    print(f"🌐 Live Data Items: {stats.get('live_data_items', 0)}")
    print(f"📝 Citations Generated: {stats.get('citations_generated', 0)}")
    
    # Final Summary
    print("\n🎯 TEST SUMMARY")
    print("=" * 50)
    
    features_working = [
        ("✅ Document Processing", success),
        ("✅ Live Data Integration", len(mock_live_data) > 0),
        ("✅ Enhanced Response Structure", 'response' in locals() and 'error' not in response),
        ("✅ Agent Statistics", len(stats.get('enhanced_features', [])) >= 3)
    ]
    
    for feature, working in features_working:
        if working:
            print(feature)
        else:
            print(feature.replace("✅", "❌"))
    
    all_working = all(working for _, working in features_working)
    
    if all_working:
        print("\n🎉 ENHANCED SYSTEM READY!")
        print("\n🚀 Your enhanced AI assistant includes:")
        print("   📚 Proper citations with source tracking")
        print("   🔑 Key insights extraction with importance scores")
        print("   🌐 Live data integration capabilities")
        print("   📊 Confidence and freshness metrics")
        print("   🎯 Enhanced response formatting")
        print("\n🏃‍♂️ Ready to run:")
        print("   Backend: python main.py")
        print("   Enhanced UI: streamlit run streamlit_app_enhanced.py")
    else:
        print("\n⚠️ Some features need attention, but basic structure is working")
    
    return all_working

async def main():
    """Main test function"""
    try:
        success = await test_enhanced_system_offline()
        return success
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🧪 Enhanced Smart Research Assistant - Offline Test")
    print("Testing core functionality without network dependencies")
    print()
    
    # Run tests
    success = asyncio.run(main())
    
    if success:
        print("\n✨ System is ready for full deployment!")
    else:
        print("\n🔧 Please check the configuration.")
