"""
Module 3: Running Locally with Ollama
======================================
Ollama is the easiest way to run models locally (like Docker for LLMs).

Key Concepts:
- Ollama provides an OpenAI-compatible endpoint
- Run models locally for privacy and cost savings
- Docker deployment for isolation
"""

import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# ============================================================================
# Ollama Setup
# ============================================================================

print("=" * 70)
print("Ollama: Docker for LLMs")
print("=" * 70)

print("""
🐋 OLLAMA CONCEPT: Like Docker, but for LLMs

Docker:
  docker pull nginx
  docker run nginx

Ollama:
  ollama pull llama3
  ollama run llama3

Both provide:
- Easy model management
- Isolated environments
- Simple CLI interface
""")


# ============================================================================
# Step 1: The Docker Command
# ============================================================================

print("\n" + "=" * 70)
print("Step 1: Running Ollama in Docker")
print("=" * 70)

print("""
📦 DOCKER COMMAND:

docker run -d \\
  -v ollama:/root/.ollama \\
  -p 11434:11434 \\
  --name ollama \\
  ollama/ollama

Breakdown:
  -d                    = Run in background
  -v ollama:...         = Persist models in volume
  -p 11434:11434        = Expose API port
  --name ollama         = Container name
  ollama/ollama         = Official image

Why Docker?
- Doesn't mess up your local OS
- Easy to remove/update
- Isolated environment
- Reproducible deployments
""")


# ============================================================================
# Step 2: Pulling a Model
# ============================================================================

print("\n" + "=" * 70)
print("Step 2: Pulling a Model")
print("=" * 70)

print("""
📥 PULL A MODEL:

docker exec -it ollama ollama run llama3

This:
1. Downloads the model (first time only)
2. Starts an interactive chat session

Available models:
- llama3 (8B)     - Meta's latest, best quality
- mistral (7B)    - Fast and efficient
- phi (2.7B)      - Smaller, faster
- codellama (7B)  - Specialized for code

Model sizes:
- 2.7B = ~1.6GB download
- 7B   = ~3.8GB download
- 8B   = ~4.7GB download
""")


# ============================================================================
# Step 3: Using with Python (OpenAI-Compatible!)
# ============================================================================

print("\n" + "=" * 70)
print("Step 3: OpenAI-Compatible Endpoint")
print("=" * 70)

print("""
🔑 KEY INSIGHT: Ollama provides an OpenAI-compatible endpoint!

This means you can use the SAME CODE for both:
- OpenAI's cloud API
- Ollama's local API

Just change the base_url!
""")

# Check if Ollama is running
import requests

try:
    response = requests.get("http://localhost:11434/api/tags", timeout=2)
    ollama_running = response.status_code == 200
except:
    ollama_running = False

if not ollama_running:
    print("\n⚠️  Ollama is not running!")
    print("\nTo start Ollama:")
    print("1. Install: brew install ollama")
    print("2. Start: ollama serve")
    print("3. Pull model: ollama pull llama3")
    print("\nThen run this script again.")
else:
    print("\n✅ Ollama is running!\n")
    
    # Create client pointing to Ollama
    client = OpenAI(
        base_url='http://localhost:11434/v1',  # Ollama endpoint
        api_key='ollama',  # Required but unused
    )
    
    print("📝 Example: Using Ollama with OpenAI client\n")
    
    # This is the SAME CODE you'd use for OpenAI!
    response = client.chat.completions.create(
        model="llama3",  # Local model
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Explain what Ollama is in one sentence."}
        ],
        temperature=0.7
    )
    
    print(f"🤖 Response:\n{response.choices[0].message.content}\n")
    
    print("💡 NOTICE: Same API, different backend!")
    print("   - OpenAI: base_url='https://api.openai.com/v1'")
    print("   - Ollama: base_url='http://localhost:11434/v1'")


# ============================================================================
# Teaching Points
# ============================================================================

print("\n" + "=" * 70)
print("🎓 KEY TEACHING POINTS")
print("=" * 70)

print("""
1. OLLAMA = DOCKER FOR LLMS
   -------------------------
   Just like Docker made containers easy, Ollama makes local LLMs easy.
   
   No need to:
   - Manually download model files
   - Set up Python environments
   - Configure GPU drivers
   - Manage dependencies
   
   Just: ollama pull <model> and you're done!

2. OPENAI-COMPATIBLE API
   ----------------------
   Ollama provides the SAME API as OpenAI.
   
   This means:
   - Same Python code works for both
   - Easy to switch between cloud and local
   - No need to learn a new API
   
   Example:
   
   # Cloud (OpenAI)
   client = OpenAI(api_key="sk-...")
   
   # Local (Ollama)
   client = OpenAI(
       base_url='http://localhost:11434/v1',
       api_key='ollama'
   )
   
   # Same code from here on!

3. WHY RUN LOCALLY?
   -----------------
   ✅ Privacy: Data never leaves your machine
   ✅ Cost: No API fees
   ✅ Offline: Works without internet
   ✅ Control: Full control over models
   ✅ Learning: Understand how models work
   
   ❌ Slower: Local hardware vs cloud GPUs
   ❌ Limited: Smaller models only
   ❌ Setup: Need to install and manage

4. DOCKER DEPLOYMENT
   ------------------
   Running in Docker:
   - Keeps your system clean
   - Easy to remove/update
   - Reproducible across machines
   - Production-ready
   
   The command:
   docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
   
   Breakdown:
   -d                 = Detached (background)
   -v ollama:...      = Volume for models
   -p 11434:11434     = Port mapping
   --name ollama      = Container name
   ollama/ollama      = Image

5. MODEL MANAGEMENT
   -----------------
   List models:
     docker exec -it ollama ollama list
   
   Pull model:
     docker exec -it ollama ollama pull llama3
   
   Remove model:
     docker exec -it ollama ollama rm llama3
   
   Run interactively:
     docker exec -it ollama ollama run llama3

6. WHEN TO USE OLLAMA
   -------------------
   ✅ Development and testing
   ✅ Privacy-sensitive applications
   ✅ Offline deployments
   ✅ Cost-sensitive projects
   ✅ Learning and experimentation
   
   ❌ Need best quality (use GPT-4)
   ❌ High throughput (use cloud)
   ❌ Limited hardware

7. COMPARISON TO CLOUD
   --------------------
   OpenAI API:
   - Fastest, best quality
   - Costs money per token
   - Requires internet
   - Data goes to OpenAI
   
   Ollama:
   - Free, unlimited usage
   - Runs offline
   - Data stays local
   - Slower, smaller models
""")

print("\n" + "=" * 70)
print("✅ Module 3 - Ollama Complete!")
print("=" * 70)
print("\nNext: Run huggingface_models.py to learn about transformers")
print("\nThen move to Module 4: Deployment with FastAPI!")
