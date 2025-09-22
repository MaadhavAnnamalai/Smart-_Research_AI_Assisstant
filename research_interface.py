#!/usr/bin/env python3
"""
Structured Research Interface
Enhanced Streamlit app for displaying structured research reports with proper citations
"""

import streamlit as st
import requests
import json
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Page config
st.set_page_config(
    page_title="AI Research Assistant",
    page_icon="🔬",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
.research-report {
    border: 1px solid #ddd;
    border-radius: 10px;
    padding: 20px;
    margin: 10px 0;
    background-color: #f9f9f9;
}

.citation-box {
    background-color: #e8f4f8;
    border-left: 4px solid #2E86C1;
    padding: 10px;
    margin: 5px 0;
    border-radius: 5px;
}

.confidence-score {
    font-size: 1.2em;
    font-weight: bold;
}

.metric-card {
    background-color: #ffffff;
    padding: 1rem;
    border-radius: 0.5rem;
    border: 1px solid #e0e0e0;
    margin: 0.5rem 0;
}

.source-tag {
    background-color: #3498db;
    color: white;
    padding: 2px 8px;
    border-radius: 12px;
    font-size: 0.8em;
    margin: 2px;
    display: inline-block;
}
</style>
""", unsafe_allow_html=True)

def display_research_report(report_data):
    """Display a structured research report"""
    
    # Header
    st.markdown("### 🔬 Research Report")
    
    # Metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="📊 Confidence Score",
            value=f"{report_data['confidencescore']:.1%}",
            help="Overall confidence in the research findings"
        )
    
    with col2:
        st.metric(
            label="🕒 Freshness Score", 
            value=f"{report_data['freshnessscore']:.1%}",
            help="How recent/fresh the data sources are"
        )
    
    with col3:
        st.metric(
            label="📚 Sources Used",
            value=len(report_data['citations']),
            help="Number of sources cited in this report"
        )
    
    with col4:
        st.metric(
            label="🔍 Key Findings",
            value=len(report_data['keyfindings']),
            help="Number of key insights extracted"
        )
    
    # Executive Summary
    st.markdown("#### 📝 Executive Summary")
    st.info(report_data['executivesummary'])
    
    # Key Findings
    st.markdown("#### 🔎 Key Findings")
    for i, finding in enumerate(report_data['keyfindings'], 1):
        st.markdown(f"**{i}.** {finding}")
    
    # Detailed Analysis
    st.markdown("#### 📖 Detailed Analysis")
    st.markdown(report_data['detailedanalysis'])
    
    # Citations
    st.markdown("#### 📚 Citations & Sources")
    
    # Create two columns for citations
    if report_data['citations']:
        for i, citation in enumerate(report_data['citations']):
            with st.expander(f"📄 {citation['source']} - {citation['title']}", expanded=False):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"**Excerpt:** {citation['excerpt']}")
                    if citation['url']:
                        st.markdown(f"**URL:** [{citation['url']}]({citation['url']})")
                with col2:
                    confidence_color = "green" if citation['confidence'] > 0.8 else "orange" if citation['confidence'] > 0.5 else "red"
                    st.markdown(f"**Confidence:** <span style='color: {confidence_color}'>{citation['confidence']:.1%}</span>", unsafe_allow_html=True)
    else:
        st.warning("No citations available for this report.")
    
    # Recommendations
    st.markdown("#### 💡 Recommendations")
    for i, rec in enumerate(report_data['recommendations'], 1):
        st.markdown(f"**{i}.** {rec}")
    
    # Sources Used (for display)
    st.markdown("#### 🗂️ Sources Overview")
    if report_data['sourcesused']:
        source_df = pd.DataFrame({
            'Source': report_data['sourcesused'],
            'Index': range(1, len(report_data['sourcesused']) + 1)
        })
        st.dataframe(source_df, use_container_width=True)
    
    # Confidence visualization
    if report_data['citations']:
        st.markdown("#### 📊 Citation Confidence Distribution")
        confidence_scores = [cite['confidence'] for cite in report_data['citations']]
        source_names = [cite['source'] for cite in report_data['citations']]
        
        fig = px.bar(
            x=source_names,
            y=confidence_scores,
            title="Citation Confidence by Source",
            labels={'x': 'Source', 'y': 'Confidence Score'},
            color=confidence_scores,
            color_continuous_scale='RdYlGn'
        )
        fig.update_layout(
            xaxis_tickangle=-45,
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)

def main():
    st.title("🔬 AI Research Assistant")
    st.markdown("**Generate structured research reports with proper citations**")
    
    # API Configuration
    API_BASE = "http://127.0.0.1:8000"
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("🔧 Configuration")
        st.info("**Research Mode**: Structured reports with citations")
        
        # API Health Check
        try:
            response = requests.get(f"{API_BASE}/api/health", timeout=2)
            if response.status_code == 200:
                health_data = response.json()
                st.success("✅ API Connected")
                st.json({
                    "Research Agent": health_data.get("research_agent_available", False),
                    "Live Data": health_data.get("services", {}).get("live_data_service", False)
                })
            else:
                st.error("❌ API Connection Failed")
        except requests.exceptions.RequestException:
            st.error("❌ API Not Available")
            st.info("Please start the API server first:\n`python start_development.py`")
    
    # Main interface tabs
    tab1, tab2, tab3 = st.tabs(["🔍 Research Query", "📚 Upload Documents", "📊 Statistics"])
    
    with tab1:
        st.header("🔍 Research Query")
        st.markdown("Ask a research question and get a structured report with proper citations.")
        
        # Research query input
        query = st.text_area(
            "🧐 What would you like to research?",
            placeholder="e.g., What are the latest developments in artificial intelligence? How does machine learning impact healthcare?",
            height=100,
            help="Enter your research question. The AI will analyze available sources and generate a structured report."
        )
        
        col1, col2 = st.columns([1, 4])
        with col1:
            research_btn = st.button("🔬 Generate Report", type="primary", use_container_width=True)
        with col2:
            if query:
                st.caption("✨ Will generate a structured research report with citations")
            else:
                st.caption("Enter a research question to get started")
        
        if research_btn and query:
            with st.spinner("🔬 Generating structured research report..."):
                try:
                    # Call the research API
                    response = requests.post(
                        f"{API_BASE}/api/research",
                        json={"message": query, "user_id": "streamlit_user"},
                        timeout=30
                    )
                    
                    if response.status_code == 200:
                        report_data = response.json()
                        
                        # Display the structured report
                        display_research_report(report_data)
                        
                        # Option to download as JSON
                        st.download_button(
                            label="💾 Download Report (JSON)",
                            data=json.dumps(report_data, indent=2),
                            file_name=f"research_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                            mime="application/json"
                        )
                        
                    else:
                        st.error(f"❌ Error generating report: {response.status_code}")
                        st.code(response.text)
                        
                except requests.exceptions.RequestException as e:
                    st.error(f"❌ Connection error: {e}")
        
        elif research_btn and not query:
            st.warning("⚠️ Please enter a research question first!")
    
    with tab2:
        st.header("📚 Upload Research Documents")
        st.markdown("Upload documents to enhance the research database.")
        
        uploaded_files = st.file_uploader(
            "📤 Choose files for research analysis",
            type=['txt', 'pdf', 'docx', 'md'],
            accept_multiple_files=True,
            help="Upload documents that will be used as sources for research reports"
        )
        
        if uploaded_files:
            col1, col2 = st.columns([1, 3])
            with col1:
                upload_btn = st.button("📚 Add to Research DB", type="primary")
            with col2:
                st.caption(f"Ready to upload {len(uploaded_files)} files to research database")
            
            if upload_btn:
                with st.spinner("📚 Processing documents for research..."):
                    try:
                        files = [("files", (file.name, file, file.type)) for file in uploaded_files]
                        
                        response = requests.post(
                            f"{API_BASE}/api/research/upload",
                            files=files,
                            timeout=60
                        )
                        
                        if response.status_code == 200:
                            result = response.json()
                            st.success(result["message"])
                            
                            # Display processed files
                            if result.get("files"):
                                st.markdown("#### ✅ Processed Files:")
                                for file_info in result["files"]:
                                    st.write(f"• **{file_info['filename']}** ({file_info['file_type']}) - {file_info['size']:,} bytes")
                        else:
                            st.error(f"❌ Upload failed: {response.status_code}")
                            
                    except requests.exceptions.RequestException as e:
                        st.error(f"❌ Connection error: {e}")
    
    with tab3:
        st.header("📊 Research Agent Statistics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🔬 Research Agent Stats")
            try:
                response = requests.get(f"{API_BASE}/api/research/stats")
                if response.status_code == 200:
                    stats = response.json()
                    
                    # Display metrics
                    st.metric("📚 Total Sources", stats.get("total_sources", 0))
                    st.metric("🧠 Vector Stores", stats.get("vector_stores", 0))
                    st.metric("📡 Live Data Items", stats.get("live_data_items", 0))
                    
                    # LLM Status
                    llm_status = "✅ Available" if stats.get("llm_available") else "❌ Not Available"
                    embeddings_status = "✅ Available" if stats.get("embeddings_available") else "❌ Not Available"
                    
                    st.write(f"**LLM Status:** {llm_status}")
                    st.write(f"**Embeddings:** {embeddings_status}")
                    
                else:
                    st.error("❌ Could not fetch research stats")
            except requests.exceptions.RequestException:
                st.error("❌ API connection failed")
        
        with col2:
            st.subheader("🔄 Update Live Data")
            st.markdown("Refresh the research database with latest live data.")
            
            if st.button("🔄 Update Live Data", type="secondary"):
                with st.spinner("🔄 Updating research database with live data..."):
                    try:
                        response = requests.post(f"{API_BASE}/api/research/live")
                        if response.status_code == 200:
                            result = response.json()
                            st.success(result["message"])
                            st.info(f"Added {result['items_added']} new items")
                        else:
                            st.error("❌ Failed to update live data")
                    except requests.exceptions.RequestException:
                        st.error("❌ Connection failed")
    
    # Footer
    st.markdown("---")
    st.markdown("🔬 **AI Research Assistant** | Structured research reports with proper citations | Powered by GPT-4")

if __name__ == "__main__":
    main()
