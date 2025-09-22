#!/usr/bin/env python3
"""
Run script for Smart Research Assistant - Conversational Edition
This script starts both the FastAPI backend and Streamlit frontend
"""

import subprocess
import sys
import time
import os
import signal
import threading
from pathlib import Path

def check_requirements():
    """Check if required packages are installed"""
    try:
        import fastapi
        import streamlit
        import langchain
        print("✅ All required packages are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing required package: {e}")
        print("Please run: pip install -r requirements_conversational.txt")
        return False

def check_env_file():
    """Check if .env file exists and has API keys"""
    env_file = Path(".env")
    if not env_file.exists():
        print("❌ .env file not found")
        print("Please run: python setup_environment.py")
        return False
    
    # Check for API keys
    with open(env_file) as f:
        content = f.read()
        if "your_openai_api_key_here" in content and "your_anthropic_api_key_here" in content:
            print("⚠️  Please configure your API keys in the .env file")
            return False
    
    print("✅ .env file configured")
    return True

def run_backend():
    """Run the FastAPI backend"""
    print("🚀 Starting FastAPI backend...")
    try:
        subprocess.run([sys.executable, "main.py"], check=True)
    except KeyboardInterrupt:
        print("\n🛑 Backend stopped")
    except Exception as e:
        print(f"❌ Backend error: {e}")

def run_frontend():
    """Run the Streamlit frontend"""
    print("🚀 Starting Streamlit frontend...")
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "streamlit_app.py"], check=True)
    except KeyboardInterrupt:
        print("\n🛑 Frontend stopped")
    except Exception as e:
        print(f"❌ Frontend error: {e}")

def main():
    """Main function to run the application"""
    print("🔬 Smart Research Assistant - Conversational Edition")
    print("=" * 60)
    
    # Check requirements
    if not check_requirements():
        sys.exit(1)
    
    # Check environment
    if not check_env_file():
        sys.exit(1)
    
    print("\n🎯 Starting application...")
    print("Backend will run on: http://localhost:8000")
    print("Frontend will run on: http://localhost:8501")
    print("\nPress Ctrl+C to stop both services")
    print("=" * 60)
    
    # Start backend in a separate thread
    backend_thread = threading.Thread(target=run_backend, daemon=True)
    backend_thread.start()
    
    # Wait a moment for backend to start
    time.sleep(3)
    
    # Start frontend (this will block)
    try:
        run_frontend()
    except KeyboardInterrupt:
        print("\n🛑 Shutting down...")
        sys.exit(0)

if __name__ == "__main__":
    main()



