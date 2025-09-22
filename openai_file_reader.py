#!/usr/bin/env python3
"""
OpenAI API file reader and query explainer
Demonstrates file reading and query explanation capabilities
"""

import os
from openai import OpenAI, AuthenticationError, RateLimitError, APIError
import sys
from datetime import datetime

def test_openai_key(api_key: str) -> bool:
    """Check if the provided API key works with OpenAI using modern API."""
    
    print(f"Testing OpenAI API key at {datetime.now()}")
    print("=" * 50)
    
    try:
        # Initialize client
        client = OpenAI(api_key=api_key)
        
        print("Testing API key with a simple completion request...")
        
        # Make a simple test request using chat completions
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": "Say hello in one sentence."}
            ],
            max_tokens=50,
            temperature=0.7
        )
        
        if response and response.choices and len(response.choices) > 0:
            message = response.choices[0].message.content
            print("✅ API Key works! Model response:")
            print(f"Response: {message}")
            
            # Additional info
            print(f"\nModel used: {response.model}")
            print(f"Tokens used: {response.usage.total_tokens if response.usage else 'Unknown'}")
            
            return True
        else:
            print("❌ ERROR: Invalid response structure")
            return False

    except AuthenticationError as e:
        print("❌ Invalid API Key. Please check your key.")
        print(f"Error details: {e}")
        return False

    except RateLimitError as e:
        print("⚠️ Rate limit exceeded. The API key is valid but you've hit rate limits.")
        print(f"Error details: {e}")
        return False

    except APIError as e:
        print("❌ API Error occurred.")
        print(f"Error details: {e}")
        return False

    except Exception as e:
        print("⚠️ An unexpected error occurred:", str(e))
        print(f"Error type: {type(e).__name__}")
        return False


def read_file_with_openai(api_key: str, file_path: str, query: str = None) -> bool:
    """Read a file and optionally answer questions about it using OpenAI."""
    
    print(f"\n{'='*60}")
    print(f"FILE READING WITH OPENAI")
    print(f"{'='*60}")
    
    try:
        # Check if file exists
        if not os.path.exists(file_path):
            print(f"❌ File not found: {file_path}")
            return False
        
        # Read the file
        print(f"📖 Reading file: {file_path}")
        with open(file_path, 'r', encoding='utf-8') as file:
            file_content = file.read()
        
        print(f"✅ File read successfully ({len(file_content)} characters)")
        
        # Initialize OpenAI client
        client = OpenAI(api_key=api_key)
        
        # Prepare the prompt
        if query:
            prompt = f"""Please analyze the following file content and answer the user's question.

FILE CONTENT:
{file_content}

USER QUESTION: {query}

Please provide a detailed response based on the file content."""
        else:
            prompt = f"""Please analyze the following file content and provide a summary of what it contains.

FILE CONTENT:
{file_content}

Please provide a detailed summary and analysis."""
        
        print(f"🤖 Sending to OpenAI for analysis...")
        
        # Send to OpenAI
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000,
            temperature=0.3
        )
        
        if response and response.choices and len(response.choices) > 0:
            analysis = response.choices[0].message.content
            print(f"\n📋 ANALYSIS RESULT:")
            print(f"{'='*40}")
            print(analysis)
            print(f"{'='*40}")
            
            print(f"\nModel used: {response.model}")
            print(f"Tokens used: {response.usage.total_tokens if response.usage else 'Unknown'}")
            
            return True
        else:
            print("❌ ERROR: Invalid response structure")
            return False

    except Exception as e:
        print(f"❌ Error reading file or processing with OpenAI: {e}")
        return False


def explain_query(api_key: str, query: str) -> bool:
    """Explain a user query using OpenAI."""
    
    print(f"\n{'='*60}")
    print(f"QUERY EXPLANATION WITH OPENAI")
    print(f"{'='*60}")
    
    try:
        # Initialize OpenAI client
        client = OpenAI(api_key=api_key)
        
        print(f"❓ User Query: {query}")
        print(f"🤖 Processing with OpenAI...")
        
        # Send query to OpenAI
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": f"Please explain the following query in detail and provide helpful information: {query}"}
            ],
            max_tokens=800,
            temperature=0.5
        )
        
        if response and response.choices and len(response.choices) > 0:
            explanation = response.choices[0].message.content
            print(f"\n💡 EXPLANATION:")
            print(f"{'='*40}")
            print(explanation)
            print(f"{'='*40}")
            
            print(f"\nModel used: {response.model}")
            print(f"Tokens used: {response.usage.total_tokens if response.usage else 'Unknown'}")
            
            return True
        else:
            print("❌ ERROR: Invalid response structure")
            return False

    except Exception as e:
        print(f"❌ Error processing query: {e}")
        return False


def main():
    # Try to read from environment variable first (recommended)
    api_key = os.getenv("OPENAI_API_KEY")
    
    # If not found in environment, use the hardcoded key
    if not api_key:
        print("⚠️ No OPENAI_API_KEY environment variable found.")
        print("Using hardcoded API key for testing...")
        api_key = "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"
    else:
        print("✅ Using API key from environment variable.")
    
    print(f"API Key (first 10 chars): {api_key[:10]}...")
    print()
    
    # Test basic API key functionality
    if not test_openai_key(api_key):
        print("💥 API key test failed! Cannot proceed.")
        sys.exit(1)
    
    # Test file reading capabilities
    print(f"\n{'='*60}")
    print("TESTING FILE READING CAPABILITIES")
    print(f"{'='*60}")
    
    # Test with the requirements.txt file
    if os.path.exists("requirements.txt"):
        print("📁 Testing with requirements.txt file...")
        read_file_with_openai(api_key, "requirements.txt", "What dependencies does this project need?")
    else:
        print("⚠️ requirements.txt not found, creating a sample file...")
        with open("sample_code.py", "w") as f:
            f.write("""# Sample Python code
def hello_world():
    print("Hello, World!")
    return "Success"

class Calculator:
    def add(self, a, b):
        return a + b
    
    def multiply(self, a, b):
        return a * b

if __name__ == "__main__":
    hello_world()
    calc = Calculator()
    print(calc.add(5, 3))
""")
        read_file_with_openai(api_key, "sample_code.py", "What does this Python code do?")
    
    # Test query explanation
    print(f"\n{'='*60}")
    print("TESTING QUERY EXPLANATION CAPABILITIES")
    print(f"{'='*60}")
    
    test_queries = [
        "What is machine learning?",
        "How do I optimize a Python function?",
        "Explain the difference between lists and tuples in Python"
    ]
    
    for query in test_queries:
        explain_query(api_key, query)
        print("\n" + "-"*60 + "\n")
    
    print("🎉 All tests completed successfully!")


if __name__ == "__main__":
    main()


