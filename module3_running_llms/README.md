# Module 3: Running & Using LLMs

## 🎯 Goal
Learn different ways to run and use LLMs: Cloud APIs, Local Models, and Hugging Face.

---

## 📚 Topics Covered

### 1. Cloud APIs (OpenAI & Gemini)
- OpenAI API setup and usage
- Gemini (Google Gen AI SDK)
- API comparison and when to use each

### 2. Running Locally (Ollama & Docker)
- **Ollama**: The easiest way to run models locally (like Docker for LLMs)
- Docker setup for isolated deployment
- OpenAI-compatible endpoint

### 3. Hugging Face & Instruction-Tuned Models
- Difference between Base vs Instruction-Tuned models
- Using `transformers` library
- Chat templates and proper formatting

---

## 🔑 Key Concepts

### Base vs Instruction-Tuned Models

**Base Model** (Autocomplete engine):
```
Input: "The capital of France is"
Output: " a beautiful city."
```

**Instruction-Tuned Model** (Chatbot):
```
Input: "The capital of France is"
Output: "Paris."
```

### Ollama - Docker for LLMs

Ollama makes running local models as easy as Docker containers:
- Pull models like `ollama pull llama3`
- Run with `ollama run llama3`
- OpenAI-compatible API endpoint

---

## 📁 Files in This Module

1. **`cloud_apis.py`** - OpenAI and Gemini comparison
2. **`ollama_local.py`** - Running Ollama locally
3. **`ollama_docker.md`** - Docker deployment guide
4. **`huggingface_models.py`** - Using transformers library
5. **`OLLAMA_GUIDE.md`** - Complete Ollama documentation

---

## 🚀 Quick Start

### Cloud APIs
```bash
python cloud_apis.py
```

### Ollama (Local)
```bash
# Install Ollama
brew install ollama  # macOS

# Start server
ollama serve

# Pull a model
ollama pull llama3

# Run Python example
python ollama_local.py
```

### Hugging Face
```bash
pip install transformers torch

python huggingface_models.py
```

---

## 🎓 Learning Objectives

By the end of this module, you will:

- ✅ Use OpenAI and Gemini APIs
- ✅ Run models locally with Ollama
- ✅ Deploy Ollama in Docker
- ✅ Understand Base vs Instruction-Tuned models
- ✅ Use Hugging Face transformers
- ✅ Format prompts for different models
- ✅ Choose the right deployment method

---

## 📊 Deployment Comparison

| Method | Cost | Privacy | Speed | Setup |
|--------|------|---------|-------|-------|
| **OpenAI API** | $$$ | Cloud | Fast | Easy |
| **Gemini API** | $ | Cloud | Fast | Easy |
| **Ollama** | Free | Local | Medium | Easy |
| **Hugging Face** | Free | Local | Slow | Medium |

---

## 🎯 Next Module

Once you can run LLMs, move to **Module 4: Deployment** to build production APIs with FastAPI!

---

**Duration**: 90 minutes  
**Difficulty**: Intermediate  
**Prerequisites**: Modules 1-2 completed
