# LLM Lecture Guide: Advanced Topics
**Date:** January 7, 2026  
**Duration:** 2-3 hours  
**Level:** Intermediate to Advanced

---

## 📋 Table of Contents

1. [Prompt Formats](#1-prompt-formats)
   - Alpaca Format
   - ChatML Format
   - LLaMA-2 Format
2. [Structured Outputs using Pydantic](#2-structured-outputs-using-pydantic)
3. [Running & Using LLMs](#3-running--using-llms)
   - OpenAI API with Python
   - Gemini API with Python
   - Running Models Locally (Ollama & Docker)
   - Hugging Face & Instruction-Tuned Models
   - Connecting LLMs to FastAPI Endpoints

---

## 1. Prompt Formats

### Why Prompt Formats Matter?
Different LLM models are trained with specific prompt templates. Using the correct format ensures:
- ✅ Better model performance
- ✅ Consistent outputs
- ✅ Proper instruction following

### 1.1 Alpaca Format

**Origin:** Stanford's Alpaca project (fine-tuned LLaMA)

**Structure:**
```
Below is an instruction that describes a task. Write a response that appropriately completes the request.

### Instruction:
{instruction}

### Input:
{input}

### Response:
{response}
```

**When to Use:**
- Alpaca-based models
- Instruction-following tasks
- Simple Q&A scenarios

**Example:**
```
Below is an instruction that describes a task. Write a response that appropriately completes the request.

### Instruction:
Summarize the following text in one sentence.

### Input:
Artificial intelligence is transforming industries worldwide. From healthcare to finance, AI systems are becoming increasingly sophisticated.

### Response:
AI is revolutionizing multiple industries globally with increasingly advanced systems.
```

**Implementation File:** `07_alpaca_format.py`

---

### 1.2 ChatML Format

**Origin:** OpenAI (used in GPT-3.5, GPT-4)

**Structure:**
```
<|im_start|>system
{system_message}<|im_end|>
<|im_start|>user
{user_message}<|im_end|>
<|im_start|>assistant
{assistant_message}<|im_end|>
```

**When to Use:**
- OpenAI models
- Multi-turn conversations
- Role-based interactions

**Example:**
```
<|im_start|>system
You are a helpful Python programming assistant.<|im_end|>
<|im_start|>user
How do I read a CSV file in Python?<|im_end|>
<|im_start|>assistant
You can use the pandas library:
import pandas as pd
df = pd.read_csv('file.csv')<|im_end|>
```

**Implementation File:** `08_chatml_format.py`

---

### 1.3 LLaMA-2 Format

**Origin:** Meta's LLaMA-2 models

**Structure:**
```
<s>[INST] <<SYS>>
{system_message}
<</SYS>>

{user_message} [/INST]
```

**For Multi-turn:**
```
<s>[INST] <<SYS>>
{system_message}
<</SYS>>

{user_message_1} [/INST] {assistant_response_1} </s><s>[INST] {user_message_2} [/INST]
```

**When to Use:**
- LLaMA-2 models
- Meta's fine-tuned variants
- Open-source deployments

**Example:**
```
<s>[INST] <<SYS>>
You are a helpful, respectful and honest assistant.
<</SYS>>

What is the capital of France? [/INST] The capital of France is Paris. </s>
```

**Implementation File:** `09_llama2_format.py`

---

## 2. Structured Outputs using Pydantic

### Why Structured Outputs?
- 🎯 **Type Safety:** Ensure outputs match expected schema
- 🔒 **Validation:** Automatic data validation
- 📊 **Parsing:** Easy JSON to Python object conversion
- 🐛 **Debugging:** Clear error messages

### Key Concepts

**Pydantic Models:**
```python
from pydantic import BaseModel, Field
from typing import List, Optional

class Person(BaseModel):
    name: str = Field(description="Full name of the person")
    age: int = Field(ge=0, le=150, description="Age in years")
    email: Optional[str] = Field(None, description="Email address")
    skills: List[str] = Field(default_factory=list)
```

### Use Cases

1. **Data Extraction:** Extract structured data from unstructured text
2. **API Responses:** Ensure consistent API output format
3. **Form Validation:** Validate user inputs
4. **Database Models:** Map LLM outputs to database schemas

### OpenAI Structured Outputs (New!)

OpenAI now supports native structured outputs:
```python
from openai import OpenAI
from pydantic import BaseModel

class CalendarEvent(BaseModel):
    name: str
    date: str
    participants: list[str]

client = OpenAI()
completion = client.beta.chat.completions.parse(
    model="gpt-4o-2024-08-06",
    messages=[
        {"role": "system", "content": "Extract the event information."},
        {"role": "user", "content": "Alice and Bob are meeting on Friday"}
    ],
    response_format=CalendarEvent,
)

event = completion.choices[0].message.parsed
```

**Implementation File:** `10_pydantic_structured_outputs.py`

---

## 3. Running & Using LLMs

### 3.1 OpenAI API with Python

**Setup:**
```bash
pip install openai python-dotenv
```

**Basic Usage:**
```python
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello!"}
    ]
)

print(response.choices[0].message.content)
```

**Advanced Features:**
- Streaming responses
- Function calling
- Vision capabilities (GPT-4V)
- JSON mode

**Implementation File:** `11_openai_advanced.py`

---

### 3.2 Gemini API with Python

**Setup:**
```bash
pip install google-generativeai
```

**Basic Usage:**
```python
import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel('gemini-pro')
response = model.generate_content("Explain quantum computing")

print(response.text)
```

**Gemini Features:**
- Multi-modal inputs (text, images, video)
- Long context window (up to 1M tokens)
- Fast inference
- Free tier available

**Implementation File:** `12_gemini_advanced.py`

---

### 3.3 Running Models Locally (Ollama & Docker)

#### Why Run Locally?
- 🔒 **Privacy:** Data stays on your machine
- 💰 **Cost:** No API fees
- 🚀 **Speed:** No network latency
- 🛠️ **Customization:** Full control over models

#### Ollama Setup

**Installation:**
```bash
# macOS
brew install ollama

# Linux
curl -fsSL https://ollama.com/install.sh | sh

# Windows
# Download from ollama.com
```

**Basic Usage:**
```bash
# Pull a model
ollama pull llama2

# Run interactively
ollama run llama2

# Run as API server
ollama serve
```

**Python Integration:**
```python
import requests

def query_ollama(prompt, model="llama2"):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": model,
            "prompt": prompt,
            "stream": False
        }
    )
    return response.json()["response"]
```

#### Docker Setup

**Dockerfile for Ollama:**
```dockerfile
FROM ollama/ollama

# Pull model during build
RUN ollama serve & sleep 5 && ollama pull llama2

EXPOSE 11434

CMD ["ollama", "serve"]
```

**Docker Compose:**
```yaml
version: '3.8'
services:
  ollama:
    image: ollama/ollama
    ports:
      - "11434:11434"
    volumes:
      - ollama_data:/root/.ollama
    restart: unless-stopped

volumes:
  ollama_data:
```

**Implementation Files:** 
- `13_ollama_local.py`
- `14_ollama_docker_setup.md`

---

### 3.4 Hugging Face & Instruction-Tuned Models

#### What are Instruction-Tuned Models?
Models specifically trained to follow instructions (e.g., Flan-T5, Alpaca, Vicuna)

**Setup:**
```bash
pip install transformers torch accelerate
```

**Using Hugging Face Transformers:**
```python
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

model_name = "meta-llama/Llama-2-7b-chat-hf"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.float16,
    device_map="auto"
)

prompt = "What is machine learning?"
inputs = tokenizer(prompt, return_tensors="pt").to("cuda")
outputs = model.generate(**inputs, max_length=200)
response = tokenizer.decode(outputs[0], skip_special_tokens=True)
```

**Popular Instruction-Tuned Models:**
- `google/flan-t5-large` (3B params)
- `meta-llama/Llama-2-7b-chat-hf` (7B params)
- `mistralai/Mistral-7B-Instruct-v0.2` (7B params)
- `HuggingFaceH4/zephyr-7b-beta` (7B params)

**Implementation File:** `15_huggingface_models.py`

---

### 3.5 Connecting LLMs to FastAPI Endpoints

#### Why FastAPI?
- ⚡ Fast and async
- 📝 Auto-generated docs
- 🔍 Type validation
- 🚀 Production-ready

**Setup:**
```bash
pip install fastapi uvicorn
```

**Basic FastAPI + OpenAI:**
```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import OpenAI
import os

app = FastAPI()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class ChatRequest(BaseModel):
    message: str
    model: str = "gpt-4o-mini"

class ChatResponse(BaseModel):
    response: str
    model: str

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        response = client.chat.completions.create(
            model=request.model,
            messages=[
                {"role": "user", "content": request.message}
            ]
        )
        return ChatResponse(
            response=response.choices[0].message.content,
            model=request.model
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Run with: uvicorn main:app --reload
```

**Advanced Features:**
- Streaming responses
- Rate limiting
- Authentication
- Caching
- Background tasks

**Implementation File:** `16_fastapi_llm_endpoint.py`

---

## 🎯 Learning Path

### Beginner → Intermediate
1. Start with OpenAI/Gemini APIs
2. Learn prompt formats
3. Implement structured outputs with Pydantic

### Intermediate → Advanced
4. Run models locally with Ollama
5. Explore Hugging Face models
6. Build production APIs with FastAPI

---

## 📚 Additional Resources

### Documentation
- [OpenAI API Docs](https://platform.openai.com/docs)
- [Google Gemini Docs](https://ai.google.dev/docs)
- [Ollama Documentation](https://ollama.com/docs)
- [Hugging Face Transformers](https://huggingface.co/docs/transformers)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)

### Tools
- [Pydantic](https://docs.pydantic.dev/)
- [LangChain](https://python.langchain.com/)
- [LlamaIndex](https://docs.llamaindex.ai/)

---

## 🛠️ Hands-On Exercises

### Exercise 1: Prompt Format Comparison
Compare the same prompt across Alpaca, ChatML, and LLaMA-2 formats

### Exercise 2: Build a Structured Extractor
Create a Pydantic model to extract contact information from emails

### Exercise 3: Local LLM Setup
Set up Ollama and run a model locally

### Exercise 4: FastAPI Chatbot
Build a simple chatbot API with rate limiting

---

## ✅ Pre-Lecture Checklist

- [ ] Install required packages (`pip install -r requirements.txt`)
- [ ] Set up API keys (OpenAI, Gemini)
- [ ] Install Ollama (optional for local models)
- [ ] Install Docker (optional for containerization)
- [ ] Test all example scripts
- [ ] Review Pydantic basics
- [ ] Familiarize with FastAPI

---

## 📝 Notes for Instructor

- **Timing:** Allocate 20-30 mins per major section
- **Demos:** Run live code examples
- **Q&A:** Reserve 10 mins at the end of each section
- **Hands-on:** Encourage students to run code alongside
- **Troubleshooting:** Have backup API keys ready

---

**Last Updated:** January 7, 2026  
**Version:** 1.0
