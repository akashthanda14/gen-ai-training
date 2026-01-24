# LLM Lecture - Quick Reference Card

## 📁 File Structure

```
prompts/
├── 07_alpaca_format.py              # Alpaca prompt format
├── 08_chatml_format.py              # ChatML prompt format
├── 09_llama2_format.py              # LLaMA-2 prompt format
├── 10_pydantic_structured_outputs.py # Pydantic for structured data
├── 11_openai_advanced.py            # OpenAI advanced features
├── 12_gemini_advanced.py            # Gemini API features
├── 13_ollama_local.py               # Local LLMs with Ollama
├── 14_ollama_docker_setup.md        # Docker deployment guide
├── 15_huggingface_models.py         # Hugging Face Transformers
├── 16_fastapi_llm_endpoint.py       # FastAPI server
└── docs/
    ├── LLM_LECTURE_GUIDE.md         # Main lecture guide
    └── LECTURE_STEPS.md             # Step-by-step instructions
```

---

## 🚀 Quick Start Commands

### Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys
```

### Run Examples
```bash
# Prompt formats
python 07_alpaca_format.py
python 08_chatml_format.py
python 09_llama2_format.py

# Structured outputs
python 10_pydantic_structured_outputs.py

# API examples
python 11_openai_advanced.py
python 12_gemini_advanced.py

# Local models
python 13_ollama_local.py
python 15_huggingface_models.py

# FastAPI server
python 16_fastapi_llm_endpoint.py
```

---

## 📋 Prompt Format Comparison

| Format | Origin | Structure | Use Case |
|--------|--------|-----------|----------|
| **Alpaca** | Stanford | `### Instruction:\n{text}\n### Response:` | Single-turn tasks |
| **ChatML** | OpenAI | `<\|im_start\|>role\n{text}<\|im_end\|>` | Multi-turn chat |
| **LLaMA-2** | Meta | `<s>[INST] {text} [/INST]` | LLaMA-2 models |

---

## 🔧 Pydantic Quick Reference

```python
from pydantic import BaseModel, Field
from typing import List, Optional

class Person(BaseModel):
    name: str = Field(description="Full name")
    age: int = Field(ge=0, le=150)
    email: Optional[str] = None
    skills: List[str] = Field(default_factory=list)

# Usage
person = Person(name="Alice", age=30, skills=["Python"])
```

---

## 🌐 API Comparison

| Feature | OpenAI | Gemini | Ollama |
|---------|--------|--------|--------|
| **Cost** | Paid | Free tier + Paid | Free (local) |
| **Context** | 128K tokens | 1M tokens | Varies by model |
| **Speed** | Fast | Very fast | Depends on hardware |
| **Privacy** | Cloud | Cloud | Local (private) |
| **Multimodal** | Text, Images | Text, Images, Video | Text only |

---

## 🤖 Model Selection Guide

### OpenAI Models
- `gpt-4o`: Most capable, multimodal
- `gpt-4o-mini`: Fast, cost-effective
- `gpt-3.5-turbo`: Legacy, cheaper

### Gemini Models
- `gemini-pro`: Text generation
- `gemini-pro-vision`: Multimodal
- `gemini-1.5-pro`: Long context (1M tokens)

### Ollama Models
```bash
ollama pull llama2        # 3.8GB - General purpose
ollama pull mistral       # 4.1GB - Strong performance
ollama pull codellama     # 3.8GB - Code generation
ollama pull phi           # 1.6GB - Smaller, faster
```

### Hugging Face Models
- `google/flan-t5-small` (80M) - Fast, learning
- `google/flan-t5-base` (250M) - Better quality
- `microsoft/phi-2` (2.7B) - Strong performance
- `mistralai/Mistral-7B-Instruct-v0.2` (7B) - Production

---

## 🔑 Environment Variables

```bash
# .env file
OPENAI_API_KEY=sk-...
GEMINI_API_KEY=AI...
API_TOKEN=demo-token-12345
```

---

## 📊 Generation Parameters

| Parameter | Range | Effect | Recommended |
|-----------|-------|--------|-------------|
| `temperature` | 0.0-2.0 | Randomness | 0.7 (balanced) |
| `max_tokens` | 1-4096+ | Length | Task-dependent |
| `top_p` | 0.0-1.0 | Nucleus sampling | 0.9 |
| `top_k` | 1-100 | Token selection | 40 |
| `presence_penalty` | -2.0-2.0 | Topic diversity | 0.0 |
| `frequency_penalty` | -2.0-2.0 | Repetition | 0.0 |

### Temperature Guide
- **0.0-0.3**: Factual, consistent (summaries, extraction)
- **0.5-0.7**: Balanced (general chat, Q&A)
- **0.8-1.0**: Creative (stories, brainstorming)
- **1.0+**: Highly creative, unpredictable

---

## 🛠️ FastAPI Endpoints

```bash
# Health check
GET /health

# List models
GET /api/v1/models

# Simple completion
POST /api/v1/completion
{
  "prompt": "What is AI?",
  "model": "gpt-4o-mini",
  "max_tokens": 100
}

# Chat completion
POST /api/v1/chat
{
  "messages": [
    {"role": "user", "content": "Hello!"}
  ],
  "model": "gpt-4o-mini"
}

# Streaming chat
POST /api/v1/chat/stream
```

### Authentication
```bash
curl -H "Authorization: Bearer demo-token-12345" \
  http://localhost:8000/api/v1/completion
```

---

## 🐛 Common Issues & Solutions

### API Key Not Found
```bash
# Check .env file exists
cat .env

# Verify loading
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print(os.getenv('OPENAI_API_KEY')[:10])"
```

### Ollama Not Running
```bash
# Start Ollama server
ollama serve

# Check status
curl http://localhost:11434/api/tags
```

### Out of Memory (Hugging Face)
```python
# Use smaller model
model_name = "google/flan-t5-small"

# Or use quantization
from transformers import BitsAndBytesConfig
config = BitsAndBytesConfig(load_in_4bit=True)
```

### Import Errors
```bash
# Reinstall packages
pip install --upgrade -r requirements.txt
```

---

## 📚 Useful Code Snippets

### OpenAI Streaming
```python
stream = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Hello"}],
    stream=True
)

for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="")
```

### Gemini Chat
```python
import google.generativeai as genai

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(history=[])

response = chat.send_message("Hello!")
print(response.text)
```

### Ollama Request
```python
import requests

response = requests.post(
    "http://localhost:11434/api/generate",
    json={
        "model": "llama2",
        "prompt": "Hello!",
        "stream": False
    }
)
print(response.json()["response"])
```

### Pydantic Validation
```python
from pydantic import BaseModel, ValidationError

class User(BaseModel):
    name: str
    age: int

try:
    user = User(name="Alice", age=30)
except ValidationError as e:
    print(e.errors())
```

---

## 🎯 Learning Checklist

- [ ] Understand Alpaca, ChatML, LLaMA-2 formats
- [ ] Create Pydantic models for validation
- [ ] Use OpenAI API with streaming
- [ ] Use Gemini API with long context
- [ ] Run Ollama locally
- [ ] Load Hugging Face models
- [ ] Build FastAPI endpoint
- [ ] Implement rate limiting
- [ ] Handle errors properly
- [ ] Choose right model for task

---

## 📖 Documentation Links

- [OpenAI API](https://platform.openai.com/docs)
- [Gemini API](https://ai.google.dev/docs)
- [Ollama](https://ollama.com/docs)
- [Hugging Face](https://huggingface.co/docs/transformers)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Pydantic](https://docs.pydantic.dev/)

---

## 💡 Pro Tips

1. **Start Small**: Test with small models before scaling
2. **Cache Locally**: Download models once, reuse
3. **Monitor Costs**: Track API usage and tokens
4. **Version Control**: Pin package versions
5. **Error Handling**: Always handle API failures
6. **Rate Limiting**: Respect API rate limits
7. **Security**: Never commit API keys
8. **Testing**: Test with different temperatures
9. **Documentation**: Read model cards carefully
10. **Community**: Join Discord/forums for help

---

**Last Updated**: January 7, 2026  
**Version**: 1.0
