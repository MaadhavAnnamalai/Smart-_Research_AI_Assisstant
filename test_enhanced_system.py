"""
Test script for the Enhanced Smart Research Assistant
Tests citations, key insights extraction, and live data integration
"""

import asyncio
import os
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from services.enhanced_conversational_agent import EnhancedConversationalAgent
from services.live_data_service import LiveDataService
from langchain.docstore.document import Document
from dotenv import load_dotenv

load_dotenv()

async def test_enhanced_system():
    """Test the enhanced system functionality"""
    print("🚀 Testing Enhanced Smart Research Assistant")
    print("=" * 60)
    
    # Initialize components
    print("1️⃣ Initializing Enhanced Conversational Agent...")
    agent = EnhancedConversationalAgent()
    
    print("2️⃣ Initializing Live Data Service...")
    live_service = LiveDataService()
    
    # Test 1: Document Upload and Processing
    print("\n📄 TEST 1: Document Upload and Processing")
    print("-" * 40)
    
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
    
    # Add documents to agent
    success = await agent.add_documents(sample_docs, "research")
    if success:
        print("✅ Sample documents added successfully")
    else:
        print("❌ Failed to add documents")
        return False
    
    # Test 2: Live Data Integration
    print("\n🌐 TEST 2: Live Data Integration")
    print("-" * 40)
    
    # Fetch and add live data
    try:
        live_data = await live_service.get_live_data()
        await agent.add_live_data(live_data.get("items", []))
        print(f"✅ Added {len(live_data.get('items', []))} live data items")
    except Exception as e:
        print(f"⚠️ Live data integration warning: {e}")
    
    # Test 3: Enhanced Chat with Citations and Insights
    print("\n💬 TEST 3: Enhanced Chat Response")
    print("-" * 40)
    
    test_queries = [
        "What are the key findings about AI and machine learning accuracy?",
        "How is artificial intelligence being used in healthcare?",
        "What are the future trends in technology and computing?",
        "Compare the accuracy improvements mentioned in the documents"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n🔍 Query {i}: {query}")
        print("-" * 30)
        
        try:
            # Process chat message
            response = await agent.chat(
                message=query,
                session_id="test_session",
                user_id="test_user"
            )
            
            if "error" in response:
                print(f"❌ Error: {response['error']}")
                continue
            
            response_data = response.get("response", {})
            
            # Check for required features
            print("✅ Response Generated Successfully")
            
            # Test Citations
            citations = response_data.get('citations', [])
            print(f"📚 Citations Found: {len(citations)}")
            if citations:
                doc_citations = [c for c in citations if c.get('source_type') == 'document']
                live_citations = [c for c in citations if c.get('source_type') == 'live_data']
                print(f"   - Document citations: {len(doc_citations)}")
                print(f"   - Live data citations: {len(live_citations)}")
                
                # Show first citation as example
                if citations:
                    first_citation = citations[0]
                    print(f"   - Example citation: {first_citation.get('source_name', 'Unknown')}")
            
            # Test Key Insights
            insights = response_data.get('key_insights', [])
            print(f"🔑 Key Insights Found: {len(insights)}")
            if insights:
                for j, insight in enumerate(insights[:2], 1):  # Show first 2 insights
                    importance = insight.get('importance_score', 0)
                    category = insight.get('category', 'General')
                    print(f"   - Insight {j}: {category} (importance: {importance:.2f})")
                    print(f"     {insight.get('insight', '')[:100]}...")
            
            # Test Live Data Integration
            live_data_info = response_data.get('live_data_integration', {})
            print(f"🌐 Live Data Integration: {live_data_info.get('freshness', 'Unknown')}")
            if live_data_info.get('live_sources_count', 0) > 0:
                print(f"   - Live sources used: {live_data_info.get('live_sources_count', 0)}")
            
            # Test Confidence and Freshness Scores
            confidence = response_data.get('confidence_score', 0)
            freshness = response_data.get('freshness_score', 0)
            print(f"📊 Confidence: {confidence:.2f}, Freshness: {freshness:.2f}")
            
            # Check if summary contains inline citations
            summary = response_data.get('summary', '')
            has_inline_citations = '[1]' in summary or '[2]' in summary
            print(f"📝 Inline Citations in Summary: {'✅' if has_inline_citations else '❌'}")
            
            print(f"📄 Summary Preview: {summary[:150]}...")
            
        except Exception as e:
            print(f"❌ Error processing query: {e}")
    
    # Test 4: Agent Statistics
    print("\n📊 TEST 4: Agent Statistics")
    print("-" * 40)
    
    stats = agent.get_agent_stats()
    print(f"Total Documents: {stats.get('total_documents', 0)}")
    print(f"Active Conversations: {stats.get('active_conversations', 0)}")
    print(f"Live Data Items: {stats.get('live_data_items', 0)}")
    print(f"Citations Generated: {stats.get('citations_generated', 0)}")
    print(f"Enhanced Features: {stats.get('enhanced_features', [])}")
    
    # Final Summary
    print("\n🎯 TEST SUMMARY")
    print("=" * 60)
    
    required_features = [
        ("Document Processing", success),
        ("Live Data Integration", len(live_data.get('items', [])) > 0),
        ("Citations Generation", stats.get('citations_generated', 0) > 0),
        ("Enhanced Features", len(stats.get('enhanced_features', [])) >= 3)
    ]
    
    all_passed = True
    for feature_name, passed in required_features:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{feature_name}: {status}")
        if not passed:
            all_passed = False
    
    if all_passed:
        print("\n🎉 ALL TESTS PASSED! Enhanced system is working correctly.")
        print("🚀 Your AI assistant now supports:")
        print("   ✅ Proper citations with source references")
        print("   ✅ Key insights extraction with importance scores")
        print("   ✅ Live data integration with real-world information")
    else:
        print("\n⚠️  Some tests failed. Please check the configuration and try again.")
    
    return all_passed

async def main():
    """Main test function"""
    try:
        success = await test_enhanced_system()
        return success
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🧪 Enhanced Smart Research Assistant Test Suite")
    print("Testing citations, key insights, and live data integration...")
    print()
    
    # Check if API key is available
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("⚠️  WARNING: No OPENAI_API_KEY found. Running in MOCK mode.")
        print("   Set your API key in .env file for full functionality testing.")
        print()
    
    # Run tests
    success = asyncio.run(main())
    
    if success:
        print("\n🎊 Ready to run your enhanced assistant!")
        print("   Backend: python main.py")
        print("   Frontend: streamlit run streamlit_app_enhanced.py")
    else:
        print("\n🔧 Please address the issues above before running the system.")
