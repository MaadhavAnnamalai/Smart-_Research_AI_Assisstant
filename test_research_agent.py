#!/usr/bin/env python3
"""
Test script for Structured Research Agent
Demonstrates the new JSON report format with proper citations
"""

import asyncio
import json
from datetime import datetime
from langchain.docstore.document import Document
from services.structured_research_agent import StructuredResearchAgent, ResearchReport

async def test_research_agent():
    """Test the structured research agent functionality"""
    print("🔬 Testing Structured Research Agent")
    print("=" * 50)
    
    # Initialize the research agent
    agent = StructuredResearchAgent()
    
    # Load test document
    print("📚 Loading test document...")
    with open("test_research_data.txt", "r", encoding="utf-8") as f:
        content = f.read()
    
    # Create document object
    doc = Document(
        page_content=content,
        metadata={"source": "AI Healthcare Research Report", "date": "2024"}
    )
    
    # Add document to agent
    success = await agent.add_documents([doc], "healthcare_research")
    print(f"✅ Document added successfully: {success}")
    
    # Test queries
    test_queries = [
        "What are the benefits of AI in healthcare?",
        "How accurate are machine learning diagnostic tools?",
        "What are the challenges of implementing AI in healthcare?"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n🔍 Test Query {i}: {query}")
        print("-" * 40)
        
        # Generate research report
        report = await agent.generate_research_report(query)
        
        # Display structured report
        print(f"📋 Topic: {report.topic}")
        print(f"📊 Confidence Score: {report.confidencescore:.2f}")
        print(f"🕒 Freshness Score: {report.freshnessscore:.2f}")
        print(f"\n📝 Executive Summary:")
        print(report.executivesummary)
        print(f"\n🔎 Key Findings:")
        for finding in report.keyfindings:
            print(f"  • {finding}")
        print(f"\n📖 Detailed Analysis:")
        print(report.detailedanalysis)
        print(f"\n💡 Recommendations:")
        for rec in report.recommendations:
            print(f"  • {rec}")
        print(f"\n📚 Citations ({len(report.citations)}):")
        for cite in report.citations:
            print(f"  [{cite.source}] {cite.title} (Confidence: {cite.confidence:.2f})")
            print(f"      Excerpt: {cite.excerpt[:100]}...")
        
        # Show JSON output
        print(f"\n🔧 JSON Output (sample):")
        try:
            json_output = report.model_dump()  # Pydantic v2 syntax
        except AttributeError:
            json_output = report.dict()  # Pydantic v1 fallback
        
        print(json.dumps({
            "topic": json_output["topic"],
            "confidencescore": json_output["confidencescore"],
            "freshnessscore": json_output["freshnessscore"],
            "citations_count": len(json_output["citations"])
        }, indent=2))
        
        print("\n" + "="*50)
    
    # Test agent stats
    stats = agent.get_agent_stats()
    print(f"\n📊 Agent Statistics:")
    print(json.dumps(stats, indent=2))

if __name__ == "__main__":
    print("🚀 Starting Structured Research Agent Test")
    asyncio.run(test_research_agent())
    print("\n✅ Test completed successfully!")
