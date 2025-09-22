#!/usr/bin/env python3
"""
Modern OpenAI API key tester with environment variable support
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
    
    success = test_openai_key(api_key)
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 API key test completed successfully!")
    else:
        print("💥 API key test failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()
