# 🎓 LLM Lecture: Complete Guide

Welcome to the comprehensive LLM lecture materials! This package contains everything you need to teach or learn advanced LLM concepts.

---

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Up API Keys
Create a `.env` file:
```bash
OPENAI_API_KEY=your_openai_key_here
GEMINI_API_KEY=your_gemini_key_here
API_TOKEN=demo-token-12345
```

### 3. Start Learning
```bash
# Read the step-by-step guide
open docs/LECTURE_STEPS.md

# Or run the first example
python 07_alpaca_format.py
```

---

## 📚 What's Included

### 📖 Documentation (4 files)
1. **LLM_LECTURE_GUIDE.md** - Main lecture guide with all theory
2. **LECTURE_STEPS.md** - Step-by-step instructions
3. **QUICK_REFERENCE_LECTURE.md** - Quick lookup reference
4. **LECTURE_SUMMARY.md** - Complete overview

### 💻 Implementation Files (10 files)

#### Prompt Formats
- `07_alpaca_format.py` - Alpaca prompt format
- `08_chatml_format.py` - ChatML format (OpenAI)
- `09_llama2_format.py` - LLaMA-2 format (Meta)

#### Structured Outputs
- `10_pydantic_structured_outputs.py` - Pydantic validation

#### API Integration
- `11_openai_advanced.py` - OpenAI advanced features
- `12_gemini_advanced.py` - Google Gemini API

#### Local Deployment
- `13_ollama_local.py` - Local LLMs with Ollama
- `14_ollama_docker_setup.md` - Docker deployment
- `15_huggingface_models.py` - Hugging Face Transformers

#### Production API
- `16_fastapi_llm_endpoint.py` - FastAPI server

---

## 🎯 Topics Covered

### 1. Prompt Formats (30 mins)
- ✅ Alpaca: Stanford's instruction format
- ✅ ChatML: OpenAI's conversation format
- ✅ LLaMA-2: Meta's specialized format

### 2. Structured Outputs (30 mins)
- ✅ Pydantic models and validation
- ✅ Type safety and constraints
- ✅ OpenAI structured outputs

### 3. Running & Using LLMs (90 mins)
- ✅ OpenAI API (streaming, functions, JSON mode)
- ✅ Gemini API (multimodal, long context)
- ✅ Ollama (local deployment)
- ✅ Hugging Face (transformers, quantization)
- ✅ FastAPI (production endpoints)

---

## 📋 Learning Path

### For Teaching
1. Review `docs/LLM_LECTURE_GUIDE.md`
2. Follow `docs/LECTURE_STEPS.md` session by session
3. Run examples live during lecture
4. Use `docs/QUICK_REFERENCE_LECTURE.md` for Q&A

### For Self-Learning
1. Start with `docs/LECTURE_STEPS.md`
2. Run each example file in order (07-16)
3. Complete exercises after each section
4. Refer to quick reference as needed

---

## 🛠️ Prerequisites

- **Python**: 3.8 or higher
- **RAM**: 8GB+ (16GB recommended)
- **Disk**: 10GB+ free space
- **API Keys**: OpenAI and/or Gemini (optional for some examples)

---

## 📊 File Structure

```
prompts/
├── 07_alpaca_format.py              # Alpaca format examples
├── 08_chatml_format.py              # ChatML format examples
├── 09_llama2_format.py              # LLaMA-2 format examples
├── 10_pydantic_structured_outputs.py # Pydantic validation
├── 11_openai_advanced.py            # OpenAI advanced features
├── 12_gemini_advanced.py            # Gemini API features
├── 13_ollama_local.py               # Local LLMs with Ollama
├── 14_ollama_docker_setup.md        # Docker deployment guide
├── 15_huggingface_models.py         # Hugging Face models
├── 16_fastapi_llm_endpoint.py       # FastAPI production server
├── requirements.txt                 # All dependencies
└── docs/
    ├── LLM_LECTURE_GUIDE.md         # Main lecture guide
    ├── LECTURE_STEPS.md             # Step-by-step instructions
    ├── QUICK_REFERENCE_LECTURE.md   # Quick reference card
    └── LECTURE_SUMMARY.md           # Complete overview
```

---

## 🎓 Example Commands

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

### Ollama Setup
```bash
# Install Ollama
brew install ollama  # macOS

# Start server
ollama serve

# Pull a model
ollama pull llama2

# Run Python example
python 13_ollama_local.py
```

### FastAPI Server
```bash
# Start server
python 16_fastapi_llm_endpoint.py

# Access docs
open http://localhost:8000/docs

# Test endpoint
curl -X POST http://localhost:8000/api/v1/completion \
  -H "Authorization: Bearer demo-token-12345" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Hello!", "model": "gpt-4o-mini"}'
```

---

## 📚 Key Concepts

### Prompt Formats
Different models expect different prompt structures:
- **Alpaca**: `### Instruction:\n{text}\n### Response:`
- **ChatML**: `<|im_start|>role\n{text}<|im_end|>`
- **LLaMA-2**: `<s>[INST] {text} [/INST]`

### Structured Outputs
Use Pydantic to ensure type-safe, validated outputs:
```python
from pydantic import BaseModel

class Person(BaseModel):
    name: str
    age: int
```

### Deployment Options
- **Cloud APIs**: OpenAI, Gemini (fast, paid)
- **Local**: Ollama, Hugging Face (private, free)
- **Production**: FastAPI (scalable, secure)

---

## 🐛 Troubleshooting

### API Keys Not Working
```bash
# Check .env file
cat .env

# Verify loading
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print(os.getenv('OPENAI_API_KEY')[:10])"
```

### Ollama Not Running
```bash
# Start Ollama
ollama serve

# Check status
curl http://localhost:11434/api/tags
```

### Import Errors
```bash
# Reinstall packages
pip install --upgrade -r requirements.txt
```

See `docs/LECTURE_STEPS.md` for detailed troubleshooting.

---

## 📖 Documentation

- **Main Guide**: `docs/LLM_LECTURE_GUIDE.md`
- **Step-by-Step**: `docs/LECTURE_STEPS.md`
- **Quick Reference**: `docs/QUICK_REFERENCE_LECTURE.md`
- **Summary**: `docs/LECTURE_SUMMARY.md`

---

## 🎯 Learning Objectives

After completing this lecture, you will be able to:

- ✅ Understand and use different prompt formats
- ✅ Create structured outputs with Pydantic
- ✅ Use OpenAI and Gemini APIs effectively
- ✅ Run LLMs locally with Ollama
- ✅ Load and use Hugging Face models
- ✅ Build production-ready FastAPI endpoints
- ✅ Implement streaming, authentication, and rate limiting
- ✅ Choose the right model and deployment method

---

## 🚀 Next Steps

1. **Start Learning**: Open `docs/LECTURE_STEPS.md`
2. **Run Examples**: Execute files 07-16 in order
3. **Practice**: Complete exercises
4. **Build**: Create your own projects
5. **Share**: Teach others what you learned

---

## 📞 Resources

### Documentation
- [OpenAI API](https://platform.openai.com/docs)
- [Gemini API](https://ai.google.dev/docs)
- [Ollama](https://ollama.com/docs)
- [Hugging Face](https://huggingface.co/docs)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Pydantic](https://docs.pydantic.dev/)

### Communities
- [OpenAI Community](https://community.openai.com/)
- [Hugging Face Forums](https://discuss.huggingface.co/)
- [FastAPI Discord](https://discord.gg/fastapi)

---

## ✨ Features

- ✅ **Comprehensive**: Covers all major LLM topics
- ✅ **Practical**: Working code examples
- ✅ **Well-Documented**: Clear explanations
- ✅ **Production-Ready**: Real-world patterns
- ✅ **Beginner-Friendly**: Step-by-step guides
- ✅ **Advanced Topics**: Streaming, quantization, etc.

---

## 📄 License

Educational use. Feel free to modify and share.

---

**Created**: January 7, 2026  
**Version**: 1.0  
**Duration**: ~3 hours  
**Level**: Intermediate to Advanced

---

## 🎉 Ready to Start!

Begin your LLM journey:

```bash
# Install dependencies
pip install -r requirements.txt

# Read the guide
open docs/LECTURE_STEPS.md

# Run first example
python 07_alpaca_format.py
```

**Happy Learning! 🚀**
