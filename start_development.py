#!/usr/bin/env python3
"""
Development startup script for AI Agent application
Runs both FastAPI backend and Streamlit frontend in development mode
"""

import os
import sys
import subprocess
import time
import signal
from pathlib import Path

def set_development_env():
    """Set development environment variables"""
    os.environ["ENVIRONMENT"] = "development"
    os.environ["DEBUG"] = "True"
    os.environ["HOST"] = "127.0.0.1"
    print("🔧 [DEVELOPMENT] Environment configured")

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import streamlit
        import fastapi
        import uvicorn
        import openai
        print("✅ [DEPENDENCIES] All required packages are installed")
        return True
    except ImportError as e:
        print(f"❌ [DEPENDENCIES] Missing required package: {e}")
        print("   Run: pip install -r requirements.txt")
        return False

def check_env_file():
    """Check if .env file exists and has required keys"""
    env_file = Path(".env")
    if not env_file.exists():
        print("❌ [CONFIG] .env file not found!")
        return False
    
    # Check for critical environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ [CONFIG] OPENAI_API_KEY not found in .env file")
        return False
    
    print("✅ [CONFIG] Environment configuration is valid")
    return True

def start_fastapi():
    """Start the FastAPI backend server in development mode"""
    print("🔧 [BACKEND] Starting FastAPI server in development mode...")
    
    # Start FastAPI with development settings (auto-reload enabled)
    process = subprocess.Popen([
        sys.executable, "main.py"
    ], cwd=os.getcwd())
    
    # Wait a moment for the server to start
    time.sleep(3)
    
    # Check if process is still running
    if process.poll() is None:
        print("✅ [BACKEND] FastAPI server started successfully")
        return process
    else:
        print("❌ [BACKEND] Failed to start FastAPI server")
        return None

def start_streamlit():
    """Start the Streamlit frontend in development mode"""
    print("🔧 [FRONTEND] Starting Streamlit server in development mode...")
    
    # Start Streamlit with development settings
    process = subprocess.Popen([
        sys.executable, "-m", "streamlit", "run", "streamlit_app.py",
        "--server.port", "8501",
        "--server.headless", "false",
        "--server.runOnSave", "true"
    ], cwd=os.getcwd())
    
    # Wait a moment for the server to start
    time.sleep(3)
    
    # Check if process is still running
    if process.poll() is None:
        print("✅ [FRONTEND] Streamlit server started successfully")
        return process
    else:
        print("❌ [FRONTEND] Failed to start Streamlit server")
        return None

def main():
    """Main development startup function"""
    print("🔧 AI Agent - Development Startup")
    print("=" * 40)
    
    # Pre-flight checks
    if not check_dependencies():
        sys.exit(1)
    
    if not check_env_file():
        sys.exit(1)
    
    # Set development environment
    set_development_env()
    
    # Start services
    fastapi_process = start_fastapi()
    if not fastapi_process:
        sys.exit(1)
    
    streamlit_process = start_streamlit()
    if not streamlit_process:
        fastapi_process.terminate()
        sys.exit(1)
    
    print("\n🎉 [SUCCESS] AI Agent is running in development mode!")
    print("=" * 50)
    print("📍 API Backend:    http://127.0.0.1:8000")
    print("📍 Web Interface:  http://localhost:8501")
    print("📍 Health Check:   http://127.0.0.1:8000/api/health")
    print("📍 API Docs:       http://127.0.0.1:8000/docs")
    print("=" * 50)
    print("💡 Auto-reload is enabled - changes will restart servers automatically")
    print("Press Ctrl+C to stop all services")
    
    def signal_handler(sig, frame):
        print("\n🛑 [SHUTDOWN] Stopping all services...")
        if fastapi_process:
            fastapi_process.terminate()
        if streamlit_process:
            streamlit_process.terminate()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Wait for processes
    try:
        while True:
            # Check if processes are still running
            if fastapi_process.poll() is not None:
                print("❌ [ERROR] FastAPI process stopped unexpectedly")
                break
            if streamlit_process.poll() is not None:
                print("❌ [ERROR] Streamlit process stopped unexpectedly")
                break
            time.sleep(1)
    except KeyboardInterrupt:
        signal_handler(None, None)

if __name__ == "__main__":
    main()
