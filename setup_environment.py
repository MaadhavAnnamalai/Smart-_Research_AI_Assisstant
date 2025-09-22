#!/usr/bin/env python3
"""
Setup script for Smart Research Assistant
This script helps configure the environment and install dependencies
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        sys.exit(1)
    print(f"✅ Python {sys.version.split()[0]} detected")

def create_env_file():
    """Create .env file from template"""
    env_file = Path(".env")
    env_example = Path("env_example.txt")
    
    if env_file.exists():
        print("✅ .env file already exists")
        return
    
    if env_example.exists():
        shutil.copy(env_example, env_file)
        print("✅ Created .env file from template")
        print("⚠️  Please edit .env file and add your API keys")
    else:
        # Create basic .env file
        with open(env_file, "w") as f:
            f.write("""# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Anthropic Configuration (Optional - for Claude)
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Database Configuration
DATABASE_URL=sqlite:///./research_assistant.db

# Application Configuration
DEBUG=True
LOG_LEVEL=INFO

# Server Configuration
HOST=0.0.0.0
PORT=8000
""")
        print("✅ Created basic .env file")
        print("⚠️  Please edit .env file and add your API keys")

def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing dependencies...")
    
    try:
        # Install from requirements file
        if Path("requirements_conversational.txt").exists():
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements_conversational.txt"], check=True)
        else:
            # Fallback to basic requirements
            subprocess.run([sys.executable, "-m", "pip", "install", 
                          "fastapi", "uvicorn", "langchain", "langchain-openai", 
                          "streamlit", "python-dotenv", "pydantic"], check=True)
        
        print("✅ Dependencies installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        sys.exit(1)

def create_directories():
    """Create necessary directories"""
    directories = ["uploads", "faiss_index", "logs"]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ Created directory: {directory}")

def check_api_keys():
    """Check if API keys are configured"""
    from dotenv import load_dotenv
    load_dotenv()
    
    openai_key = os.getenv("OPENAI_API_KEY")
    anthropic_key = os.getenv("ANTHROPIC_API_KEY")
    
    if not openai_key and not anthropic_key:
        print("⚠️  No API keys found in .env file")
        print("   Please add at least one of:")
        print("   - OPENAI_API_KEY=your_key_here")
        print("   - ANTHROPIC_API_KEY=your_key_here")
        return False
    
    if openai_key and openai_key != "your_openai_api_key_here":
        print("✅ OpenAI API key configured")
    else:
        print("⚠️  OpenAI API key not configured")
    
    if anthropic_key and anthropic_key != "your_anthropic_api_key_here":
        print("✅ Anthropic API key configured")
    else:
        print("⚠️  Anthropic API key not configured")
    
    return True

def main():
    """Main setup function"""
    print("🚀 Setting up Smart Research Assistant...")
    print("=" * 50)
    
    # Check Python version
    check_python_version()
    
    # Create .env file
    create_env_file()
    
    # Install dependencies
    install_dependencies()
    
    # Create directories
    create_directories()
    
    # Check API keys
    print("\n" + "=" * 50)
    print("🔑 API Key Configuration")
    print("=" * 50)
    api_keys_configured = check_api_keys()
    
    print("\n" + "=" * 50)
    print("🎉 Setup Complete!")
    print("=" * 50)
    
    if api_keys_configured:
        print("\n✅ Ready to run!")
        print("\nTo start the application:")
        print("1. Backend: python main.py")
        print("2. Frontend: streamlit run streamlit_app.py")
    else:
        print("\n⚠️  Please configure your API keys in the .env file")
        print("Then run the application with:")
        print("1. Backend: python main.py")
        print("2. Frontend: streamlit run streamlit_app.py")

if __name__ == "__main__":
    main()

