"""
06. Using Google Gemini API
===========================
This example shows how to use Google's Gemini API instead of OpenAI.
Different providers have different APIs, but the concepts remain the same.

Key Concepts:
- Different LLM providers (OpenAI, Google, Anthropic, etc.)
- API differences between providers
- Same prompting techniques work across providers

Note: You need a GEMINI_API_KEY in your .env file for this to work.
Get one from: https://ai.google.dev/

IMPORTANT: As of 2026, google.generativeai is deprecated.
This example uses the legacy package for compatibility but shows a warning.
For production, migrate to google.genai package.
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Validate API key is present
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    print("❌ ERROR: GEMINI_API_KEY is not set.")
    print("\nTo fix this:")
    print("1. Get an API key from: https://ai.google.dev/")
    print("2. Add it to your .env file:")
    print("   GEMINI_API_KEY=your_key_here")
    exit(1)

try:
    # Note: google.generativeai is deprecated but still works
    # For new projects, use google.genai instead
    import google.generativeai as genai
    
    # Configure Gemini API
    genai.configure(api_key=api_key)
    
    # Create a Gemini model
    model = genai.GenerativeModel('gemini-pro')
    
    print("🤖 Generating response from Gemini...\n")
    
    # Make a request to Gemini
    # Note: The API structure is different from OpenAI, but the prompt is the same
    response = model.generate_content(
        "Write a 300-word essay on Large Language Models (LLMs)"
    )
    
    # Display the response
    print(response.text)
    
except ImportError:
    print("❌ ERROR: google-generativeai package not installed.")
    print("\nTo fix this:")
    print("  pip3 install google-generativeai")
    exit(1)
    
except Exception as e:
    error_message = str(e)
    
    if "429" in error_message or "RATE_LIMIT_EXCEEDED" in error_message:
        print("❌ ERROR: Gemini API Rate Limit Exceeded")
        print("\nYour API key has hit its quota limit.")
        print("\nPossible solutions:")
        print("1. Wait a few minutes and try again")
        print("2. Check your quota at: https://console.cloud.google.com/")
        print("3. Request a quota increase")
        print("4. Get a new API key from: https://ai.google.dev/")
        print("\nNote: Free tier has limited requests per minute.")
    elif "401" in error_message or "UNAUTHENTICATED" in error_message:
        print("❌ ERROR: Invalid API Key")
        print("\nYour GEMINI_API_KEY is invalid or expired.")
        print("Get a new one from: https://ai.google.dev/")
    else:
        print(f"❌ ERROR: {error_message}")
        print("\nFor help, visit: https://ai.google.dev/docs")
    
    exit(1)

