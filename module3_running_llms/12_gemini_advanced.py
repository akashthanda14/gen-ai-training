"""
12. Gemini Advanced Features
=============================
Demonstrates advanced Google Gemini API features including multi-modal
inputs, long context, streaming, and safety settings.

Key Concepts:
- Multi-modal inputs (text, images, video)
- Long context window (up to 1M tokens)
- Streaming responses
- Safety settings and content filtering
- System instructions
"""

import os
from dotenv import load_dotenv
import google.generativeai as genai
from pathlib import Path

load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))


# Example 1: Basic Text Generation
print("=" * 60)
print("Example 1: Basic Gemini Text Generation")
print("=" * 60)

model = genai.GenerativeModel('gemini-pro')

response = model.generate_content("Explain quantum computing in simple terms.")

print(f"\n🤖 Response:\n{response.text}\n")


# Example 2: Streaming Responses
print("=" * 60)
print("Example 2: Streaming Responses")
print("=" * 60)

print("\n🔄 Streaming response:\n")

response_stream = model.generate_content(
    "Write a haiku about machine learning.",
    stream=True
)

for chunk in response_stream:
    print(chunk.text, end="", flush=True)

print("\n")


# Example 3: Multi-turn Conversation (Chat)
print("=" * 60)
print("Example 3: Multi-turn Chat")
print("=" * 60)

chat = model.start_chat(history=[])

messages = [
    "Hello! I want to learn about Python.",
    "What are the main data types?",
    "Can you show me an example of a list?"
]

for user_message in messages:
    print(f"\n👤 User: {user_message}")
    
    response = chat.send_message(user_message)
    print(f"🤖 Gemini: {response.text}")

print()


# Example 4: System Instructions (Gemini 1.5+)
print("=" * 60)
print("Example 4: System Instructions")
print("=" * 60)

# Create model with system instruction
model_with_instruction = genai.GenerativeModel(
    'gemini-pro',
    system_instruction="You are a helpful coding assistant. Always provide code examples in Python. Be concise and clear."
)

response = model_with_instruction.generate_content(
    "How do I read a JSON file?"
)

print(f"\n🤖 Response with System Instruction:\n{response.text}\n")


# Example 5: Temperature and Generation Config
print("=" * 60)
print("Example 5: Generation Configuration")
print("=" * 60)

generation_config = {
    "temperature": 0.9,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 200,
}

model_configured = genai.GenerativeModel(
    'gemini-pro',
    generation_config=generation_config
)

response = model_configured.generate_content(
    "Write a creative story opening about a robot."
)

print(f"\n🤖 Creative Response (temp=0.9):\n{response.text}\n")


# Example 6: Safety Settings
print("=" * 60)
print("Example 6: Safety Settings")
print("=" * 60)

from google.generativeai.types import HarmCategory, HarmBlockThreshold

safety_settings = {
    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
}

model_safe = genai.GenerativeModel(
    'gemini-pro',
    safety_settings=safety_settings
)

response = model_safe.generate_content(
    "Explain the importance of online safety for children."
)

print(f"\n🤖 Response:\n{response.text}")

# Check safety ratings
print(f"\n🛡️  Safety Ratings:")
for rating in response.candidates[0].safety_ratings:
    print(f"  {rating.category.name}: {rating.probability.name}")

print()


# Example 7: Counting Tokens
print("=" * 60)
print("Example 7: Token Counting")
print("=" * 60)

prompt = "Explain the theory of relativity in detail."

# Count tokens before sending
token_count = model.count_tokens(prompt)
print(f"\n📊 Token Count:")
print(f"  Prompt: '{prompt}'")
print(f"  Tokens: {token_count.total_tokens}\n")


# Example 8: Multiple Candidates
print("=" * 60)
print("Example 8: Generating Multiple Candidates")
print("=" * 60)

generation_config_multi = {
    "candidate_count": 3,  # Generate 3 different responses
    "temperature": 0.9,
}

try:
    model_multi = genai.GenerativeModel(
        'gemini-pro',
        generation_config=generation_config_multi
    )
    
    response = model_multi.generate_content(
        "Suggest a creative name for a coffee shop."
    )
    
    print(f"\n💡 Generated {len(response.candidates)} suggestions:\n")
    for i, candidate in enumerate(response.candidates, 1):
        print(f"  {i}. {candidate.content.parts[0].text}")
    
except Exception as e:
    print(f"\n⚠️  Multiple candidates not available: {e}")
    print("Generating single response instead...\n")
    
    response = model.generate_content(
        "Suggest a creative name for a coffee shop."
    )
    print(f"💡 Suggestion: {response.text}")

print()


# Example 9: JSON Output
print("=" * 60)
print("Example 9: Structured JSON Output")
print("=" * 60)

import json

json_prompt = """
Extract the following information from this text and return as JSON:
Text: "Sarah Johnson is a 28-year-old software engineer living in Seattle. 
She specializes in machine learning and has 5 years of experience."

Return JSON with fields: name, age, occupation, location, specialization, years_experience
"""

response = model.generate_content(json_prompt)

try:
    # Try to parse as JSON
    data = json.loads(response.text)
    print(f"\n📋 Extracted JSON:")
    print(json.dumps(data, indent=2))
except json.JSONDecodeError:
    print(f"\n📋 Response:\n{response.text}")

print()


# Example 10: Long Context (Gemini 1.5 Pro)
print("=" * 60)
print("Example 10: Long Context Handling")
print("=" * 60)

# Gemini 1.5 Pro supports up to 1M tokens
long_text = """
Artificial Intelligence (AI) has transformed numerous industries over the past decade.
From healthcare to finance, transportation to entertainment, AI systems are becoming
increasingly sophisticated and integrated into our daily lives.

Machine learning, a subset of AI, enables systems to learn from data without explicit
programming. Deep learning, using neural networks with multiple layers, has achieved
remarkable results in image recognition, natural language processing, and game playing.

The ethical implications of AI are significant. Issues such as bias in algorithms,
privacy concerns, job displacement, and the potential for misuse require careful
consideration. Researchers and policymakers are working to develop frameworks for
responsible AI development and deployment.

Looking ahead, AI is expected to continue advancing rapidly. Emerging areas include
quantum machine learning, neuromorphic computing, and artificial general intelligence (AGI).
The integration of AI with other technologies like blockchain, IoT, and 5G will create
new possibilities and challenges.
""" * 10  # Repeat to create longer context

model_long = genai.GenerativeModel('gemini-pro')

response = model_long.generate_content(
    f"Summarize the following text in 3 bullet points:\n\n{long_text}"
)

print(f"\n📄 Long Text Summary:")
print(response.text)
print()


# Example 11: Prompt Feedback
print("=" * 60)
print("Example 11: Prompt Feedback and Safety")
print("=" * 60)

response = model.generate_content("Explain blockchain technology.")

print(f"\n🤖 Response:\n{response.text}")

# Check if prompt was blocked
if response.prompt_feedback:
    print(f"\n⚠️  Prompt Feedback:")
    print(f"  Block Reason: {response.prompt_feedback.block_reason}")
    print(f"  Safety Ratings: {response.prompt_feedback.safety_ratings}")
else:
    print(f"\n✅ No safety issues detected")

print()


# Best Practices
print("=" * 60)
print("📚 Gemini API - Best Practices")
print("=" * 60)
print("""
1. Model Selection:
   ✅ gemini-pro: Text generation
   ✅ gemini-pro-vision: Multi-modal (text + images)
   ✅ gemini-1.5-pro: Long context (1M tokens)
   ✅ gemini-1.5-flash: Fast, efficient

2. Generation Config:
   ✅ temperature (0.0-2.0): Control randomness
   ✅ top_p (0.0-1.0): Nucleus sampling
   ✅ top_k: Limit token selection
   ✅ max_output_tokens: Control length

3. Safety Settings:
   ✅ Configure harm categories
   ✅ Set block thresholds
   ✅ Monitor safety ratings
   ✅ Handle blocked content gracefully

4. Context Management:
   ✅ Use chat for multi-turn conversations
   ✅ Leverage long context for large documents
   ✅ Count tokens to stay within limits
   ✅ Clear chat history when needed

5. System Instructions:
   ✅ Define behavior and persona
   ✅ Set output format expectations
   ✅ Specify domain expertise
   ✅ Keep instructions clear and concise

6. Streaming:
   ✅ Use for real-time applications
   ✅ Improve user experience
   ✅ Handle chunks properly
   ✅ Implement error handling

Gemini Advantages:
- Free tier available
- Long context window (1M tokens)
- Multi-modal capabilities
- Fast inference
- Strong safety features
- Competitive pricing

When to Use Gemini:
- Long document analysis
- Multi-modal applications
- Cost-sensitive projects
- Google Cloud integration
- Safety-critical applications
""")


# Comparison with OpenAI
print("=" * 60)
print("📊 Gemini vs OpenAI Comparison")
print("=" * 60)
print("""
Context Window:
- Gemini 1.5 Pro: Up to 1M tokens
- GPT-4 Turbo: 128K tokens
- GPT-4o: 128K tokens

Pricing (as of 2026):
- Gemini Pro: Free tier + paid
- GPT-4o-mini: $0.15/$0.60 per 1M tokens
- GPT-4o: $5/$15 per 1M tokens

Multi-modal:
- Gemini: Native support (text, image, video)
- OpenAI: GPT-4V (text, image)

Speed:
- Gemini Flash: Very fast
- GPT-4o-mini: Fast
- GPT-4o: Moderate

Use Gemini for:
✅ Very long documents
✅ Video analysis
✅ Cost optimization
✅ Google ecosystem integration

Use OpenAI for:
✅ Function calling
✅ Structured outputs
✅ Mature ecosystem
✅ Advanced reasoning
""")
