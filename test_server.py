#!/usr/bin/env python3
"""
Test script to verify FastAPI server starts correctly
"""

import asyncio
import sys
import time
import subprocess
import requests
import threading
from datetime import datetime

def start_server():
    """Start the FastAPI server in a subprocess"""
    try:
        process = subprocess.Popen([
            sys.executable, "main.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return process
    except Exception as e:
        print(f"❌ Failed to start server: {e}")
        return None

def test_health_endpoint():
    """Test the health endpoint"""
    max_retries = 10
    for i in range(max_retries):
        try:
            response = requests.get("http://localhost:8000/api/health", timeout=5)
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Health check passed!")
                print(f"   Status: {data['status']}")
                print(f"   Services: {data['services']}")
                return True
        except requests.exceptions.RequestException:
            if i < max_retries - 1:
                print(f"⏳ Waiting for server... ({i+1}/{max_retries})")
                time.sleep(2)
            continue
    
    print(f"❌ Health check failed after {max_retries} attempts")
    return False

def main():
    print("🚀 Testing FastAPI Server Startup...")
    print(f"   Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    # Start server
    print("1. Starting FastAPI server...")
    server_process = start_server()
    
    if not server_process:
        print("❌ Failed to start server process")
        return False
    
    try:
        # Give server time to start
        print("2. Waiting for server to initialize...")
        time.sleep(5)
        
        # Check if process is still running
        if server_process.poll() is not None:
            stdout, stderr = server_process.communicate()
            print("❌ Server process terminated unexpectedly")
            print("STDOUT:", stdout.decode())
            print("STDERR:", stderr.decode())
            return False
        
        # Test health endpoint
        print("3. Testing health endpoint...")
        success = test_health_endpoint()
        
        if success:
            print("✅ FastAPI server is running successfully!")
            print("🌐 Available endpoints:")
            print("   - http://localhost:8000/")
            print("   - http://localhost:8000/api/health")
            print("   - http://localhost:8000/api/chat")
            print("   - http://localhost:8000/docs (API documentation)")
        
        return success
        
    finally:
        # Clean up
        print("4. Stopping server...")
        server_process.terminate()
        server_process.wait(timeout=5)
        print("✅ Server stopped")

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
