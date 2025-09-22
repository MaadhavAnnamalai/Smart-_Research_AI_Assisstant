#!/usr/bin/env python3
"""
Script to help enable real mode with API keys
"""

import os
from pathlib import Path

def check_env_file():
    """Check if .env file exists and has API keys"""
    env_file = Path(".env")
    
    if not env_file.exists():
        print("❌ .env file not found")
        print("Creating .env file from template...")
        
        # Copy from example
        example_file = Path("env_example.txt")
        if example_file.exists():
            with open(example_file, 'r') as src, open(env_file, 'w') as dst:
                dst.write(src.read())
            print("✅ Created .env file from template")
        else:
            # Create basic .env file
            with open(env_file, 'w') as f:
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
        
        print("\n⚠️  Please edit .env file and add your API keys")
        return False
    
    # Check for API keys
    with open(env_file) as f:
        content = f.read()
        
    has_openai = "OPENAI_API_KEY=sk-" in content
    has_anthropic = "ANTHROPIC_API_KEY=sk-ant-" in content
    
    if not has_openai and not has_anthropic:
        print("❌ No valid API keys found in .env file")
        print("\nTo enable real mode, you need to add at least one API key:")
        print("1. Get OpenAI API key: https://platform.openai.com/api-keys")
        print("2. Get Anthropic API key: https://console.anthropic.com/")
        print("3. Edit .env file and replace 'your_*_api_key_here' with your actual key")
        return False
    
    if has_openai:
        print("✅ OpenAI API key found")
    if has_anthropic:
        print("✅ Anthropic API key found")
    
    return True

def test_real_mode():
    """Test if real mode is working"""
    print("\n--- Testing Real Mode ---")
    
    try:
        from services.simple_conversational_agent import SimpleConversationalAgent
        agent = SimpleConversationalAgent()
        
        if agent.llm is not None:
            print("✅ LLM initialized successfully")
            print(f"✅ Using: {type(agent.llm).__name__}")
        else:
            print("❌ LLM not initialized")
            return False
            
        if agent.embeddings is not None:
            print("✅ Embeddings initialized successfully")
        else:
            print("❌ Embeddings not initialized")
            return False
            
        # Simplified agent doesn't use agent_executor
        print("✅ Agent ready for conversational AI")
            
        print("\n🎉 Real mode is working! You now have:")
        print("✅ AI-powered document analysis")
        print("✅ Vector search capabilities")
        print("✅ Intelligent conversational responses")
        print("✅ Real-time data integration")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing real mode: {e}")
        return False

def main():
    print("🚀 Smart Research Assistant - Real Mode Setup")
    print("=" * 50)
    
    # Check environment
    if not check_env_file():
        print("\n📝 Next steps:")
        print("1. Get an API key from OpenAI or Anthropic")
        print("2. Edit the .env file with your actual API key")
        print("3. Run this script again to test")
        return
    
    # Test real mode
    if test_real_mode():
        print("\n🎉 Setup complete! You can now run:")
        print("python run_conversational_app.py")
    else:
        print("\n❌ Setup failed. Please check your API keys and try again.")

if __name__ == "__main__":
    main()
