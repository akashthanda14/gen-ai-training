"""
13. Running LLMs Locally with Ollama
=====================================
Demonstrates how to run LLMs locally using Ollama for privacy,
cost savings, and offline usage.

Key Concepts:
- Setting up Ollama
- Running models locally
- Python integration with Ollama
- Model management
- Streaming responses

Prerequisites:
1. Install Ollama: https://ollama.com
   - macOS: brew install ollama
   - Linux: curl -fsSL https://ollama.com/install.sh | sh
   - Windows: Download from ollama.com

2. Start Ollama server: ollama serve

3. Pull a model: ollama pull llama2
"""

import requests
import json
import time


# Configuration
OLLAMA_BASE_URL = "http://localhost:11434"


def check_ollama_status():
    """Check if Ollama server is running."""
    try:
        response = requests.get(f"{OLLAMA_BASE_URL}/api/tags")
        return response.status_code == 200
    except requests.exceptions.ConnectionError:
        return False


def list_local_models():
    """List all locally available models."""
    try:
        response = requests.get(f"{OLLAMA_BASE_URL}/api/tags")
        if response.status_code == 200:
            models = response.json().get("models", [])
            return models
        return []
    except Exception as e:
        print(f"Error listing models: {e}")
        return []


def generate_response(prompt, model="llama2", stream=False):
    """
    Generate a response using Ollama.
    
    Args:
        prompt: The input prompt
        model: Model name (e.g., "llama2", "mistral", "codellama")
        stream: Whether to stream the response
    
    Returns:
        Generated text response
    """
    url = f"{OLLAMA_BASE_URL}/api/generate"
    
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": stream
    }
    
    if stream:
        response = requests.post(url, json=payload, stream=True)
        full_response = ""
        
        for line in response.iter_lines():
            if line:
                chunk = json.loads(line)
                if "response" in chunk:
                    print(chunk["response"], end="", flush=True)
                    full_response += chunk["response"]
        
        print()  # New line after streaming
        return full_response
    else:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            return response.json()["response"]
        else:
            return f"Error: {response.status_code}"


def chat_completion(messages, model="llama2", stream=False):
    """
    Chat completion using Ollama (similar to OpenAI format).
    
    Args:
        messages: List of message dicts with 'role' and 'content'
        model: Model name
        stream: Whether to stream the response
    
    Returns:
        Assistant's response
    """
    url = f"{OLLAMA_BASE_URL}/api/chat"
    
    payload = {
        "model": model,
        "messages": messages,
        "stream": stream
    }
    
    if stream:
        response = requests.post(url, json=payload, stream=True)
        full_response = ""
        
        for line in response.iter_lines():
            if line:
                chunk = json.loads(line)
                if "message" in chunk and "content" in chunk["message"]:
                    content = chunk["message"]["content"]
                    print(content, end="", flush=True)
                    full_response += content
        
        print()
        return full_response
    else:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            return response.json()["message"]["content"]
        else:
            return f"Error: {response.status_code}"


# Check if Ollama is running
print("=" * 60)
print("Ollama Status Check")
print("=" * 60)

if not check_ollama_status():
    print("""
⚠️  Ollama server is not running!

To start Ollama:
1. Install Ollama from https://ollama.com
2. Run: ollama serve
3. In another terminal, pull a model: ollama pull llama2

Then run this script again.
""")
    exit(1)

print("✅ Ollama server is running!\n")


# List available models
print("=" * 60)
print("Available Local Models")
print("=" * 60)

models = list_local_models()

if models:
    print(f"\n📦 Found {len(models)} local model(s):\n")
    for model in models:
        name = model.get("name", "Unknown")
        size = model.get("size", 0) / (1024**3)  # Convert to GB
        print(f"  • {name} ({size:.2f} GB)")
    print()
else:
    print("""
⚠️  No models found!

To download a model:
  ollama pull llama2        # 3.8GB
  ollama pull mistral       # 4.1GB
  ollama pull codellama     # 3.8GB
  ollama pull phi           # 1.6GB (smaller, faster)

Then run this script again.
""")
    exit(1)


# Example 1: Simple Generation
print("=" * 60)
print("Example 1: Simple Text Generation")
print("=" * 60)

prompt1 = "Explain what a neural network is in one paragraph."
print(f"\n📝 Prompt: {prompt1}\n")
print("🤖 Response:")

response1 = generate_response(prompt1, model="llama2", stream=False)
print(response1)
print()


# Example 2: Streaming Response
print("=" * 60)
print("Example 2: Streaming Response")
print("=" * 60)

prompt2 = "Write a haiku about artificial intelligence."
print(f"\n📝 Prompt: {prompt2}\n")
print("🤖 Streaming Response:")

generate_response(prompt2, model="llama2", stream=True)
print()


# Example 3: Chat Completion
print("=" * 60)
print("Example 3: Chat Completion")
print("=" * 60)

messages = [
    {"role": "system", "content": "You are a helpful Python programming assistant."},
    {"role": "user", "content": "How do I read a CSV file in Python?"}
]

print("\n💬 Chat Messages:")
for msg in messages:
    print(f"  [{msg['role'].upper()}]: {msg['content']}")

print("\n🤖 Response:")
response3 = chat_completion(messages, model="llama2", stream=False)
print(response3)
print()


# Example 4: Multi-turn Conversation
print("=" * 60)
print("Example 4: Multi-turn Conversation")
print("=" * 60)

conversation = [
    {"role": "system", "content": "You are a helpful math tutor."}
]

questions = [
    "What is the Pythagorean theorem?",
    "Can you give me an example?",
    "How is this used in real life?"
]

for i, question in enumerate(questions, 1):
    print(f"\n--- Turn {i} ---")
    print(f"👤 User: {question}")
    
    conversation.append({"role": "user", "content": question})
    
    response = chat_completion(conversation, model="llama2", stream=False)
    print(f"🤖 Assistant: {response}")
    
    conversation.append({"role": "assistant", "content": response})

print()


# Example 5: Code Generation
print("=" * 60)
print("Example 5: Code Generation")
print("=" * 60)

code_prompt = "Write a Python function to calculate the factorial of a number using recursion. Include docstring and type hints."

print(f"\n📝 Prompt: {code_prompt}\n")
print("🤖 Response:")

# Use codellama if available, otherwise llama2
available_model_names = [m.get("name", "") for m in models]
code_model = "codellama" if any("codellama" in name for name in available_model_names) else "llama2"

response5 = generate_response(code_prompt, model=code_model, stream=False)
print(response5)
print()


# Example 6: Different Models Comparison
print("=" * 60)
print("Example 6: Model Comparison")
print("=" * 60)

comparison_prompt = "Explain quantum computing in one sentence."

print(f"\n📝 Prompt: {comparison_prompt}\n")

# Test with available models
test_models = ["llama2", "mistral", "phi"]

for model_name in test_models:
    # Check if model is available
    if any(model_name in m.get("name", "") for m in models):
        print(f"🤖 {model_name.upper()}:")
        try:
            response = generate_response(comparison_prompt, model=model_name, stream=False)
            print(f"   {response}\n")
        except Exception as e:
            print(f"   Error: {e}\n")


# Example 7: Temperature Control
print("=" * 60)
print("Example 7: Temperature Control")
print("=" * 60)

creative_prompt = "Write a creative opening line for a sci-fi story."

print(f"\n📝 Prompt: {creative_prompt}\n")

temperatures = [0.0, 0.5, 1.0]

for temp in temperatures:
    print(f"🌡️  Temperature {temp}:")
    
    url = f"{OLLAMA_BASE_URL}/api/generate"
    payload = {
        "model": "llama2",
        "prompt": creative_prompt,
        "stream": False,
        "options": {
            "temperature": temp
        }
    }
    
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        print(f"   {response.json()['response']}\n")


# Example 8: Model Information
print("=" * 60)
print("Example 8: Model Information")
print("=" * 60)

def get_model_info(model_name):
    """Get detailed information about a model."""
    url = f"{OLLAMA_BASE_URL}/api/show"
    payload = {"name": model_name}
    
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        return None

if models:
    first_model = models[0].get("name", "")
    print(f"\n📊 Information for: {first_model}\n")
    
    info = get_model_info(first_model)
    if info:
        print(f"  Model: {info.get('modelfile', 'N/A')[:100]}...")
        print(f"  Parameters: {info.get('parameters', 'N/A')}")
    else:
        print("  Could not retrieve model info")

print()


# Best Practices
print("=" * 60)
print("📚 Ollama Best Practices")
print("=" * 60)
print("""
1. Model Selection:
   ✅ llama2 (7B): General purpose, good balance
   ✅ mistral (7B): Strong performance, efficient
   ✅ codellama (7B): Specialized for code
   ✅ phi (2.7B): Smaller, faster, less capable
   ✅ llama2:13b: More capable, slower

2. Performance Optimization:
   ✅ Use smaller models for faster inference
   ✅ Adjust temperature for creativity vs consistency
   ✅ Use streaming for better UX
   ✅ Keep context length reasonable

3. Hardware Requirements:
   ✅ 8GB RAM: Run 7B models
   ✅ 16GB RAM: Run 13B models comfortably
   ✅ 32GB+ RAM: Run 70B models
   ✅ GPU: Significantly faster (optional)

4. Privacy & Security:
   ✅ All data stays local
   ✅ No internet required (after download)
   ✅ No API keys needed
   ✅ Full control over models

5. Use Cases:
   ✅ Sensitive data processing
   ✅ Offline applications
   ✅ Cost-sensitive projects
   ✅ Development and testing
   ✅ Learning and experimentation

Advantages of Local LLMs:
- 🔒 Complete privacy
- 💰 No API costs
- 🚀 No rate limits
- 📡 Works offline
- 🛠️ Full customization

Disadvantages:
- 💻 Requires local resources
- 🐌 Slower than cloud APIs
- 📦 Large model downloads
- 🧠 Less capable than GPT-4

Commands Reference:
  ollama pull <model>     # Download a model
  ollama list             # List local models
  ollama rm <model>       # Remove a model
  ollama run <model>      # Run model interactively
  ollama serve            # Start API server
""")


# Cleanup message
print("=" * 60)
print("✅ Ollama Examples Complete!")
print("=" * 60)
print("""
To explore more:
1. Try different models: ollama pull mistral
2. Run interactively: ollama run llama2
3. Check documentation: https://ollama.com/docs
4. Browse models: https://ollama.com/library
""")
