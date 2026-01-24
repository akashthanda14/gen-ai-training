# 🎓 Gen AI with Python - Complete Teaching Curriculum

A structured teaching plan moving from **Concepts** (Prompting) → **Implementation** (Running Models) → **Deployment** (FastAPI).

---

## 📚 Course Structure

### Module 1: The "Hidden" Language of LLMs (Prompt Formats)
**Duration**: 30 minutes | **Difficulty**: Beginner

Learn that LLMs don't just "understand" chat - they expect specific raw string formats.

- ✅ Alpaca Format (Stanford)
- ✅ ChatML Format (OpenAI)  
- ✅ LLaMA-2 Format (Meta)

**Key Insight**: Using the wrong format = poor performance!

[📁 Go to Module 1](./module1_prompt_formats/)

---

### Module 2: Structured Outputs using Pydantic
**Duration**: 30 minutes | **Difficulty**: Intermediate

Move beyond parsing messy strings. Force LLMs to speak "Code" (JSON) instead of "English."

- ✅ The problem with string parsing
- ✅ Pydantic models for validation
- ✅ **instructor** library (industry standard)
- ✅ Type-safe responses

**Key Insight**: `response_model` gives you typed Python objects!

[📁 Go to Module 2](./module2_structured_outputs/)

---

### Module 3: Running & Using LLMs
**Duration**: 90 minutes | **Difficulty**: Intermediate

Learn different ways to run LLMs: Cloud APIs, Local Models, and Hugging Face.

- ✅ OpenAI & Gemini APIs
- ✅ Ollama (Docker for LLMs)
- ✅ Hugging Face Transformers
- ✅ Base vs Instruction-Tuned Models

**Key Insight**: Ollama provides OpenAI-compatible endpoints!

[📁 Go to Module 3](./module3_running_llms/)

---

### Module 4: Deployment with FastAPI
**Duration**: 30 minutes | **Difficulty**: Advanced

Build production-ready backends. Learn the CRITICAL concept of async/await.

- ✅ Blocking vs Non-Blocking
- ✅ `async def` and `await`
- ✅ Streaming Responses
- ✅ Production patterns

**Key Insight**: `def` = one user at a time, `async def` = concurrent users!

[📁 Go to Module 4](./module4_deployment/)

---

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Up Environment
```bash
# Create .env file
cp .env.example .env

# Add your API keys
OPENAI_API_KEY=your_key_here
GEMINI_API_KEY=your_key_here
```

### 3. Start Learning
```bash
# Module 1: Prompt Formats
cd module1_prompt_formats
python alpaca_format.py

# Module 2: Structured Outputs
cd ../module2_structured_outputs
python basic_instructor.py

# Module 3: Running LLMs
cd ../module3_running_llms
python ollama_local.py

# Module 4: Deployment
cd ../module4_deployment
python async_streaming.py
```

---

## 📊 Tools Summary

| Task | Tool | Why? |
|------|------|------|
| **Prompting** | Raw Strings | Understand what the model sees |
| **Structure** | instructor | Modern, Pythonic way to handle outputs |
| **Local Run** | Ollama | Easiest zero-setup local inference |
| **Deployment** | FastAPI | Native async support required for LLM latency |

---

## 🎯 Learning Path

```
Module 1: Prompt Formats (30 min)
    ↓
Module 2: Structured Outputs (30 min)
    ↓
Module 3: Running LLMs (90 min)
    ↓
Module 4: FastAPI Deployment (30 min)
    ↓
🎓 Ready to build production LLM applications!
```

---

## 📁 Project Structure

```
prompts/
├── module1_prompt_formats/
│   ├── README.md
│   ├── alpaca_format.py
│   ├── chatml_format.py
│   └── llama2_format.py
│
├── module2_structured_outputs/
│   ├── README.md
│   └── basic_instructor.py
│
├── module3_running_llms/
│   ├── README.md
│   └── ollama_local.py
│
├── module4_deployment/
│   ├── README.md
│   └── async_streaming.py
│
├── requirements.txt
└── README.md (this file)
```

---

## 🔑 Key Concepts

### 1. Prompt Formats Matter
```python
# Wrong format = poor performance
prompt = "Tell me about AI"  # ❌

# Right format for LLaMA-2
prompt = "<s>[INST] Tell me about AI [/INST]"  # ✅
```

### 2. Structured Outputs
```python
# Without instructor
response = client.chat.completions.create(...)
text = response.choices[0].message.content  # String ❌

# With instructor
user = client.chat.completions.create(
    response_model=UserInfo,  # ✅
    ...
)
# user.name is typed!
```

### 3. Ollama = Docker for LLMs
```bash
# Pull and run models locally
ollama pull llama3
ollama run llama3

# OpenAI-compatible API!
client = OpenAI(base_url='http://localhost:11434/v1')
```

### 4. Async/Await is Required
```python
# Blocking (BAD)
def chat(prompt):  # ❌ One user at a time
    response = client.chat.completions.create(...)
    
# Non-blocking (GOOD)
async def chat(prompt):  # ✅ Concurrent users
    response = await client.chat.completions.create(...)
```

---

## 🎓 Teaching Tips

### Module 1: Prompt Formats
- **Show** the raw strings with `repr()`
- **Demonstrate** what happens with wrong format
- **Compare** all three formats side-by-side

### Module 2: Structured Outputs
- **Start** with the problem (messy string parsing)
- **Show** manual JSON parsing failures
- **Reveal** instructor as the solution

### Module 3: Running LLMs
- **Explain** Base vs Instruction-Tuned clearly
- **Demo** Ollama's ease of use
- **Highlight** OpenAI-compatible endpoint

### Module 4: FastAPI
- **Demonstrate** blocking vs non-blocking
- **Use** two terminals to show concurrent handling
- **Stream** responses to show real-time output

---

## 🛠️ Prerequisites

- **Python**: 3.8 or higher
- **API Keys**: OpenAI and/or Gemini (for cloud examples)
- **Docker**: Optional, for Ollama container deployment
- **RAM**: 8GB+ recommended for local models

---

## 📖 Additional Resources

### Documentation
- [OpenAI API](https://platform.openai.com/docs)
- [Instructor Library](https://python.useinstructor.com/)
- [Ollama](https://ollama.com/docs)
- [FastAPI](https://fastapi.tiangolo.com/)

### Model Cards
- [LLaMA-2](https://huggingface.co/meta-llama/Llama-2-7b-chat-hf)
- [Mistral](https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.2)
- [Qwen](https://huggingface.co/Qwen)

---

## ✅ Learning Checklist

After completing all modules, you should be able to:

- [ ] Explain why prompt formats exist
- [ ] Format prompts for Alpaca, ChatML, and LLaMA-2
- [ ] Use instructor for structured outputs
- [ ] Create Pydantic models with validation
- [ ] Run models locally with Ollama
- [ ] Understand Base vs Instruction-Tuned models
- [ ] Use async/await in FastAPI
- [ ] Implement streaming responses
- [ ] Deploy production-ready LLM APIs

---

## 🎯 Next Steps

1. **Complete all modules** in order
2. **Build a project** combining all concepts
3. **Deploy to production** using what you learned
4. **Share your knowledge** - teach others!

---

## 📞 Support

For questions or issues:
1. Check module READMEs
2. Review code comments
3. Consult official documentation
4. Ask in community forums

---

**Created**: January 2026  
**Version**: 1.0  
**Total Duration**: ~3 hours  
**Level**: Beginner to Advanced

---

## 🎉 Ready to Start!

Begin with Module 1:
```bash
cd module1_prompt_formats
python alpaca_format.py
```

**Happy Learning! 🚀**
