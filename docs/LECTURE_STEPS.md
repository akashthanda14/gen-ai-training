# LLM Lecture: Step-by-Step Guide

## 🎯 Objective
Master advanced LLM concepts including prompt formats, structured outputs, and various deployment methods.

---

## 📋 Prerequisites

### 1. System Requirements
- Python 3.8 or higher
- 8GB+ RAM (16GB recommended)
- 10GB+ free disk space
- Internet connection for API calls

### 2. API Keys Setup

Create a `.env` file in the project root:

```bash
# OpenAI API Key
OPENAI_API_KEY=your_openai_key_here

# Gemini API Key
GEMINI_API_KEY=your_gemini_key_here

# FastAPI Authentication Token
API_TOKEN=demo-token-12345
```

**Get API Keys:**
- OpenAI: https://platform.openai.com/api-keys
- Gemini: https://makersuite.google.com/app/apikey

### 3. Install Dependencies

```bash
# Navigate to project directory
cd /Users/work/Desktop/LLM/GEN-AI/prompts

# Install all required packages
pip install -r requirements.txt

# Verify installation
python -c "import openai, google.generativeai; print('✅ All packages installed')"
```

---

## 📚 Part 1: Prompt Formats (30 mins)

### Session 1.1: Alpaca Format

**Theory (10 mins):**
- Origin: Stanford's Alpaca project
- Structure: Instruction → Input → Response
- Use cases: Single-turn instruction following

**Practice (20 mins):**

```bash
# Run the Alpaca format examples
python 07_alpaca_format.py
```

**Key Takeaways:**
- ✅ Clear separation of instruction and input
- ✅ Best for instruction-tuned models
- ✅ Simple, consistent format

**Exercise:**
Create your own Alpaca-formatted prompt for:
1. Text summarization
2. Data extraction
3. Code generation

---

### Session 1.2: ChatML Format

**Theory (10 mins):**
- Origin: OpenAI (GPT-3.5, GPT-4)
- Structure: Role-based messaging
- Use cases: Multi-turn conversations

**Practice (20 mins):**

```bash
# Run the ChatML format examples
python 08_chatml_format.py
```

**Key Takeaways:**
- ✅ Native OpenAI format
- ✅ Excellent for chatbots
- ✅ Clear role separation (system, user, assistant)

**Exercise:**
Build a multi-turn conversation:
1. System: Define a persona
2. User: Ask 3 related questions
3. Observe context retention

---

### Session 1.3: LLaMA-2 Format

**Theory (10 mins):**
- Origin: Meta's LLaMA-2
- Structure: Special tokens (<s>, [INST], etc.)
- Use cases: LLaMA-2 models

**Practice (20 mins):**

```bash
# Run the LLaMA-2 format examples
python 09_llama2_format.py
```

**Key Takeaways:**
- ✅ Specific to LLaMA-2-Chat
- ✅ Requires exact token placement
- ✅ Supports single and multi-turn

**Exercise:**
Compare the same prompt across all three formats:
- Alpaca
- ChatML
- LLaMA-2

---

## 📚 Part 2: Structured Outputs (30 mins)

### Session 2.1: Pydantic Basics

**Theory (10 mins):**
- What is Pydantic?
- Type validation and constraints
- Benefits for LLM outputs

**Practice (20 mins):**

```bash
# Run Pydantic examples
python 10_pydantic_structured_outputs.py
```

**Key Concepts:**
- ✅ BaseModel for schema definition
- ✅ Field() for constraints
- ✅ Automatic validation
- ✅ JSON schema generation

**Exercise:**
Create a Pydantic model for:
1. Product information (name, price, category)
2. User profile (name, age, email, skills)
3. Event data (title, date, participants)

---

### Session 2.2: OpenAI Structured Outputs

**Theory (5 mins):**
- Native structured output support
- JSON mode vs. parse mode
- Error handling

**Practice (15 mins):**

Test different extraction scenarios:
1. Simple data extraction
2. Nested objects
3. Lists of objects

**Key Takeaways:**
- ✅ Guaranteed valid JSON
- ✅ Type-safe outputs
- ✅ Easy database integration

---

## 📚 Part 3: OpenAI Advanced (30 mins)

### Session 3.1: Advanced Features

**Practice:**

```bash
# Run OpenAI advanced examples
python 11_openai_advanced.py
```

**Topics Covered:**
1. **Streaming Responses** - Real-time output
2. **Function Calling** - Tool integration
3. **JSON Mode** - Structured outputs
4. **Token Management** - Cost optimization
5. **Temperature Control** - Creativity tuning

**Exercise:**
Implement a function-calling example:
1. Define 2-3 custom functions
2. Create prompts that trigger them
3. Process the results

---

## 📚 Part 4: Gemini API (20 mins)

### Session 4.1: Gemini Features

**Practice:**

```bash
# Run Gemini examples
python 12_gemini_advanced.py
```

**Topics Covered:**
1. **Multi-modal Inputs** - Text, images, video
2. **Long Context** - Up to 1M tokens
3. **Safety Settings** - Content filtering
4. **System Instructions** - Behavior control

**Key Differences from OpenAI:**
- ✅ Longer context window
- ✅ Free tier available
- ✅ Multi-modal native support
- ✅ Strong safety features

---

## 📚 Part 5: Local LLMs with Ollama (30 mins)

### Session 5.1: Ollama Setup

**Installation:**

```bash
# macOS
brew install ollama

# Linux
curl -fsSL https://ollama.com/install.sh | sh

# Start Ollama server
ollama serve
```

**Pull a Model:**

```bash
# In a new terminal
ollama pull llama2        # 3.8GB
ollama pull mistral       # 4.1GB
ollama pull phi           # 1.6GB (smaller)
```

**Practice:**

```bash
# Run Ollama examples
python 13_ollama_local.py
```

**Key Takeaways:**
- ✅ Complete privacy
- ✅ No API costs
- ✅ Works offline
- ✅ Full control

---

### Session 5.2: Docker Deployment

**Read the Guide:**

```bash
# Open the Docker setup guide
open 14_ollama_docker_setup.md
```

**Practice (Optional):**

```bash
# Create docker-compose.yml
docker-compose up -d

# Pull model in container
docker-compose exec ollama ollama pull llama2

# Test API
curl http://localhost:11434/api/generate -d '{
  "model": "llama2",
  "prompt": "Hello!",
  "stream": false
}'
```

---

## 📚 Part 6: Hugging Face Models (30 mins)

### Session 6.1: Transformers Library

**Practice:**

```bash
# Run Hugging Face examples
python 15_huggingface_models.py
```

**Topics Covered:**
1. **Pipeline API** - Simplified interface
2. **Model Loading** - From Hugging Face Hub
3. **Quantization** - Memory optimization
4. **Task-Specific Models** - Classification, QA, etc.

**Popular Models:**
- Flan-T5 (80M-11B) - Instruction-tuned
- Mistral-7B - Strong performance
- Phi-2 (2.7B) - Efficient
- LLaMA-2 (7B-70B) - Meta's models

**Exercise:**
1. Load a small model (Flan-T5-Small)
2. Test different tasks
3. Compare with API-based models

---

## 📚 Part 7: FastAPI Integration (30 mins)

### Session 7.1: Building an API

**Practice:**

```bash
# Run FastAPI server
python 16_fastapi_llm_endpoint.py
```

**Access Documentation:**
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

**Test Endpoints:**

```bash
# Health check
curl http://localhost:8000/health

# Simple completion
curl -X POST http://localhost:8000/api/v1/completion \
  -H "Authorization: Bearer demo-token-12345" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "What is FastAPI?",
    "model": "gpt-4o-mini",
    "max_tokens": 100
  }'

# Chat completion
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Authorization: Bearer demo-token-12345" \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {"role": "user", "content": "Hello!"}
    ],
    "model": "gpt-4o-mini"
  }'
```

**Key Features:**
- ✅ Authentication (Bearer token)
- ✅ Rate limiting
- ✅ Streaming support
- ✅ Error handling
- ✅ Auto-generated docs

---

## 🎓 Learning Path Summary

### Beginner → Intermediate
1. ✅ Understand prompt formats
2. ✅ Use OpenAI/Gemini APIs
3. ✅ Implement structured outputs

### Intermediate → Advanced
4. ✅ Run local models (Ollama)
5. ✅ Use Hugging Face Transformers
6. ✅ Build production APIs (FastAPI)

---

## 📝 Hands-On Exercises

### Exercise 1: Prompt Format Comparison (15 mins)
Create the same prompt in all three formats and compare results.

### Exercise 2: Data Extraction Pipeline (20 mins)
Build a pipeline that:
1. Takes unstructured text
2. Extracts structured data with Pydantic
3. Validates and stores results

### Exercise 3: Local vs Cloud Comparison (20 mins)
Compare the same task using:
- OpenAI API
- Gemini API
- Ollama (local)

Measure: speed, quality, cost

### Exercise 4: Build a Chatbot API (30 mins)
Create a FastAPI endpoint that:
1. Accepts chat messages
2. Maintains conversation history
3. Returns streaming responses
4. Implements rate limiting

---

## 🐛 Troubleshooting

### API Key Issues
```bash
# Check if .env file exists
cat .env

# Verify keys are loaded
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print(os.getenv('OPENAI_API_KEY')[:10])"
```

### Import Errors
```bash
# Reinstall packages
pip install --upgrade -r requirements.txt
```

### Ollama Connection Issues
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Restart Ollama
killall ollama
ollama serve
```

### Memory Issues (Hugging Face)
```python
# Use smaller models
model_name = "google/flan-t5-small"  # Instead of large models

# Or use quantization
from transformers import BitsAndBytesConfig
quantization_config = BitsAndBytesConfig(load_in_4bit=True)
```

---

## 📊 Assessment Checklist

After completing the lecture, you should be able to:

- [ ] Explain the differences between Alpaca, ChatML, and LLaMA-2 formats
- [ ] Create Pydantic models for structured outputs
- [ ] Use OpenAI and Gemini APIs effectively
- [ ] Run LLMs locally with Ollama
- [ ] Load and use Hugging Face models
- [ ] Build a FastAPI endpoint for LLMs
- [ ] Implement streaming responses
- [ ] Handle errors and rate limiting
- [ ] Choose the right model for a task
- [ ] Optimize for cost and performance

---

## 📚 Additional Resources

### Documentation
- [OpenAI API Docs](https://platform.openai.com/docs)
- [Gemini API Docs](https://ai.google.dev/docs)
- [Ollama Docs](https://ollama.com/docs)
- [Hugging Face Docs](https://huggingface.co/docs)
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Pydantic Docs](https://docs.pydantic.dev/)

### Communities
- [OpenAI Community](https://community.openai.com/)
- [Hugging Face Forums](https://discuss.huggingface.co/)
- [FastAPI Discord](https://discord.gg/fastapi)

### Learning Platforms
- [Hugging Face Course](https://huggingface.co/learn)
- [DeepLearning.AI](https://www.deeplearning.ai/)
- [Fast.ai](https://www.fast.ai/)

---

## 🎯 Next Steps

1. **Practice Daily**: Run at least one example per day
2. **Build Projects**: Apply concepts to real problems
3. **Join Communities**: Ask questions, share learnings
4. **Stay Updated**: Follow LLM news and updates
5. **Experiment**: Try different models and techniques

---

## ✅ Lecture Complete!

You now have a comprehensive understanding of:
- Prompt engineering formats
- Structured outputs with Pydantic
- Multiple LLM deployment methods
- Production-ready API development

**Keep learning and building! 🚀**
