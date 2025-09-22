#!/usr/bin/env python3
"""
Test script to verify Streamlit app functionality
"""

import subprocess
import sys
import time
import os

def test_streamlit_app():
    """Test if the Streamlit app can be imported and run."""
    try:
        # Test import
        print("Testing Streamlit app import...")
        import streamlit_app
        print("✅ Streamlit app imports successfully")
        
        # Test OpenAI functionality
        print("Testing OpenAI integration...")
        from streamlit_app import analyze_file, explain_query
        
        # Test with a simple query
        result = explain_query("What is Python?")
        if "Python" in result and "❌" not in result:
            print("✅ OpenAI integration works")
        else:
            print("❌ OpenAI integration failed")
            print(f"Result: {result}")
        
        print("\n🎉 Streamlit app is ready!")
        print("\nTo run the app, use:")
        print("streamlit run streamlit_app.py")
        print("\nThen open your browser to:")
        print("http://localhost:8501")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing Streamlit app: {e}")
        return False

if __name__ == "__main__":
    test_streamlit_app()


