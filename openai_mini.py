#!/usr/bin/env python3
"""
Mini OpenAI API tool - File reader and query explainer
Efficient and streamlined version
"""

import os
from openai import OpenAI, AuthenticationError
import sys

def setup_client():
    """Setup OpenAI client with API key."""
    api_key = os.getenv("OPENAI_API_KEY") or "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"
    return OpenAI(api_key=api_key)

def read_file(file_path, query=None):
    """Read file and analyze with OpenAI."""
    try:
        if not os.path.exists(file_path):
            return f"❌ File not found: {file_path}"
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        client = setup_client()
        
        prompt = f"Analyze this file content{' and answer: ' + query if query else ' and provide a summary'}:\n\n{content}"
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500,
            temperature=0.3
        )
        
        return response.choices[0].message.content
        
    except AuthenticationError:
        return "❌ Invalid API key"
    except Exception as e:
        return f"❌ Error: {e}"

def explain_query(query):
    """Explain a user query using OpenAI."""
    try:
        client = setup_client()
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": f"Explain: {query}"}],
            max_tokens=400,
            temperature=0.5
        )
        
        return response.choices[0].message.content
        
    except AuthenticationError:
        return "❌ Invalid API key"
    except Exception as e:
        return f"❌ Error: {e}"

def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python openai_mini.py file <filepath> [question]")
        print("  python openai_mini.py query <your question>")
        return
    
    command = sys.argv[1].lower()
    
    if command == "file":
        if len(sys.argv) < 3:
            print("❌ Please provide a file path")
            return
        
        file_path = sys.argv[2]
        question = sys.argv[3] if len(sys.argv) > 3 else None
        
        print(f"📖 Reading: {file_path}")
        result = read_file(file_path, question)
        print(result)
        
    elif command == "query":
        if len(sys.argv) < 3:
            print("❌ Please provide a question")
            return
        
        question = " ".join(sys.argv[2:])
        print(f"❓ Question: {question}")
        result = explain_query(question)
        print(result)
        
    else:
        print("❌ Unknown command. Use 'file' or 'query'")

if __name__ == "__main__":
    main()


