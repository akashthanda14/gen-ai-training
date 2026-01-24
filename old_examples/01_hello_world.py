"""
01. Hello World - Basic LLM API Call
====================================
This is the simplest example of calling an LLM API.
It demonstrates how to make a basic request to OpenAI's GPT model.

Key Concepts:
- Setting up the OpenAI client
- Making a simple chat completion request
- Understanding the message structure (user and system roles)
"""

import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

# Initialize the OpenAI client with API key from environment
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)

# Make a simple chat completion request
# The model will respond to the user's question
response = client.chat.completions.create(
    model="gpt-4o-mini",  # Specify which model to use
    messages=[
        # System message defines the AI's behavior/role
        {
            "role": "system",
            "content": "You are a helpful math expert. You only answer math questions. If the user asks anything else, politely decline."
        },
        # User message is the actual query
        {
            "role": "user",
            "content": "Explain the BODMAS Rule?"
        }
    ]
)

# Print the AI's response
print(response.choices[0].message.content)













# choices = [
#     {   # choice #0
#         "index": 0,
#         "message": {
#             "role": "assistant",
#             "content": "Hello! How can I help you?"
#         },
#         "finish_reason": "stop"
#     }
# ]
