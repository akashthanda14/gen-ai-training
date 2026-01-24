# Project Organization Summary

## ✅ What Was Done

### 🔧 Fixed Issues:
1. **Removed hardcoded API keys** - All keys now use environment variables
2. **Fixed typos and formatting** - Cleaned up all code
3. **Removed duplicate files** - Consolidated into organized structure
4. **Added comprehensive comments** - Every file is well-documented
5. **Standardized naming** - Files numbered 01-06 for teaching order

### 📁 New File Structure:

```
prompts/
├── 01_hello_world.py                 # Basic LLM API call
├── 02_zero_shot_prompting.py         # Direct instructions
├── 03_few_shot_prompting.py          # Learning from examples
├── 04_chain_of_thought.py            # Step-by-step reasoning
├── 05_persona_based_prompting.py     # AI with personality
├── 06_gemini_example.py              # Alternative LLM provider
├── README.md                          # Main documentation
├── QUICK_REFERENCE.md                 # Quick tips and templates
├── TEACHING_CHECKLIST.md              # Session-by-session guide
├── requirements.txt                   # Python dependencies
├── .env.example                       # API key template
├── .gitignore                         # Protect sensitive files
└── .env                               # Your actual API keys (not tracked)
```

### 🗑️ Removed Old Files:
- `chainOfThough.py` → Replaced by `04_chain_of_thought.py`
- `fewshot.py` → Replaced by `03_few_shot_prompting.py`
- `persona.py` → Replaced by `05_persona_based_prompting.py`
- `zeroshot.py` → Replaced by `02_zero_shot_prompting.py`
- `cot-Auto.py` → Empty file, removed
- `hello_world/` → Consolidated into `01_hello_world.py`
- `zero_shot_prompting/` → Consolidated into `02_zero_shot_prompting.py`
- `__pycache__/` → Removed (will be ignored by .gitignore)

---

## 📚 Documentation Created

### 1. README.md (Main Guide)
**Contents:**
- Overview of all techniques
- Setup instructions
- Detailed explanation of each technique
- Running examples
- Comprehensive teaching guide
- Troubleshooting section
- FAQ

**Use for:** Primary reference for students and instructors

### 2. QUICK_REFERENCE.md
**Contents:**
- When to use each technique
- Comparison tables
- Cost optimization tips
- Prompt templates
- Common mistakes
- Exercise solutions

**Use for:** Quick lookup during coding

### 3. TEACHING_CHECKLIST.md
**Contents:**
- Pre-class preparation
- Session-by-session plans (4 sessions)
- Hands-on exercises
- Assessment criteria
- Learning outcomes
- Teaching tips

**Use for:** Instructor's session planning

---

## 🎯 Teaching Progression

### Session 1: Foundations
- Introduction to LLMs
- Basic API calls
- System vs user roles

### Session 2: Prompting Techniques
- Zero-shot prompting
- Few-shot prompting
- When to use each

### Session 3: Advanced Techniques
- Chain-of-thought reasoning
- Persona-based prompting
- Combining techniques

### Session 4: Production Ready
- Different LLM providers
- Best practices
- Security and optimization

---

## 🔑 Key Improvements

### Security:
✅ No hardcoded API keys
✅ Environment variables only
✅ .gitignore protects .env
✅ .env.example as template

### Code Quality:
✅ Comprehensive comments
✅ Clear variable names
✅ Consistent formatting
✅ Error handling

### Documentation:
✅ Step-by-step setup guide
✅ Explanation of every technique
✅ Real-world examples
✅ Troubleshooting help

### Teaching Support:
✅ Progressive difficulty
✅ Hands-on exercises
✅ Assessment criteria
✅ Session plans

---

## 🚀 How to Use This for Teaching

### Before Class:
1. Review `README.md` thoroughly
2. Check `TEACHING_CHECKLIST.md` for session plan
3. Test all examples work
4. Prepare your API keys

### During Class:
1. Follow session plans in `TEACHING_CHECKLIST.md`
2. Use `QUICK_REFERENCE.md` for quick answers
3. Run examples live
4. Let students experiment

### After Class:
1. Share all documentation
2. Assign exercises from checklist
3. Provide feedback
4. Answer questions

---

## 📊 File Statistics

| File | Lines | Purpose |
|------|-------|---------|
| `01_hello_world.py` | 42 | Basic API introduction |
| `02_zero_shot_prompting.py` | 47 | Direct prompting |
| `03_few_shot_prompting.py` | 58 | Example-based learning |
| `04_chain_of_thought.py` | 107 | Step-by-step reasoning |
| `05_persona_based_prompting.py` | 79 | Character creation |
| `06_gemini_example.py` | 33 | Alternative provider |
| `README.md` | 450+ | Main documentation |
| `QUICK_REFERENCE.md` | 250+ | Quick tips |
| `TEACHING_CHECKLIST.md` | 400+ | Teaching guide |

**Total:** ~1,500 lines of code and documentation

---

## ✅ Quality Checklist

- [x] All code runs without errors
- [x] No hardcoded secrets
- [x] Comprehensive comments
- [x] Clear documentation
- [x] Teaching materials included
- [x] Security best practices
- [x] Beginner-friendly
- [x] Progressive difficulty
- [x] Real-world examples
- [x] Troubleshooting guide

---

## 🎓 Learning Outcomes

Students who complete this course will be able to:

1. ✅ Understand LLM API basics
2. ✅ Write effective prompts
3. ✅ Choose appropriate techniques
4. ✅ Implement zero-shot prompting
5. ✅ Implement few-shot prompting
6. ✅ Use chain-of-thought reasoning
7. ✅ Create AI personas
8. ✅ Handle API keys securely
9. ✅ Optimize for cost
10. ✅ Build real applications

---

## 📞 Next Steps

### For Instructors:
1. Review all documentation
2. Test examples with your API key
3. Customize examples for your audience
4. Prepare additional exercises if needed
5. Set up class environment

### For Students:
1. Read `README.md` setup section
2. Install dependencies
3. Configure API keys
4. Run `01_hello_world.py` to verify setup
5. Start with Session 1 exercises

---

## 🎉 Summary

**Everything is now:**
- ✅ Fixed and working
- ✅ Properly organized
- ✅ Well-documented
- ✅ Ready to teach
- ✅ Secure and professional
- ✅ Beginner-friendly

**You can now teach prompt engineering with confidence!**

---

## 📝 Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set up API key
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY

# 3. Test setup
python 01_hello_world.py

# 4. Start teaching!
# Follow TEACHING_CHECKLIST.md
```

---

# Hugging Face and Ollama: Building RAG Systems (A Practical Guide)

This tutorial teaches you about Hugging Face and Ollama, two powerful tools for working with large language models (LLMs). We'll focus on Retrieval-Augmented Generation (RAG), but with a twist: instead of just explaining RAG theoretically, we'll build a simple RAG system step-by-step using both tools. This hands-on approach will help you see how they differ and work together.

## What is Hugging Face?

Hugging Face is an open-source platform and library for machine learning, especially natural language processing (NLP). It's like a "GitHub for AI models" where you can:
- Download and use pre-trained models (e.g., BERT, GPT-like models).
- Fine-tune models on your data.
- Share your own models with the community.

Key library: `transformers` (install with `pip install transformers`).

### Quick Example: Using a Hugging Face Model
```python
from transformers import pipeline

# Load a pre-trained model for text generation
generator = pipeline("text-generation", model="gpt2")
result = generator("Hello, world!")
print(result[0]['generated_text'])
```

## What is Ollama?

Ollama is a tool for running LLMs locally on your machine. It's great for privacy and offline use. You can:
- Download and run models like Llama, Gemma, or Mistral locally.
- Use a simple command-line interface or API.
- Integrate with apps (e.g., via REST API).

Key feature: Runs models without needing a cloud API (like OpenAI). Install from [ollama.ai](https://ollama.ai).

### Quick Example: Running Ollama
```bash
# Install Ollama, then pull a model
ollama pull gemma:2b

# Run a chat
ollama run gemma:2b
# Type: "What is AI?" and get a response
```

## What is RAG? (Retrieval-Augmented Generation)

RAG is a technique to make LLMs smarter by combining them with external knowledge. Instead of relying only on the model's training data, RAG:
1. **Retrieves** relevant information from a knowledge base (e.g., documents, databases).
2. **Augments** the LLM's prompt with that info.
3. **Generates** a better, more accurate response.

Why "different" here? Traditional RAG tutorials focus on theory or cloud tools. We'll build a local RAG system using Hugging Face for retrieval and Ollama for generation—keeping everything private and offline.

## Building a Simple RAG System with Hugging Face and Ollama

We'll create a RAG chatbot that answers questions about a custom document (e.g., a text file). Hugging Face will handle retrieval (finding relevant text chunks), and Ollama will generate answers.

### Step 1: Set Up Your Environment
- Install dependencies:
  ```bash
  pip install transformers faiss-cpu sentence-transformers requests
  ```
- Install Ollama and pull a model:
  ```bash
  ollama pull gemma:2b
  ```

### Step 2: Prepare Your Knowledge Base
Create a text file (e.g., `knowledge.txt`) with info you want to retrieve from:
```
RAG stands for Retrieval-Augmented Generation. It helps LLMs answer questions using external data.
Hugging Face provides tools for NLP tasks like text embedding.
Ollama runs LLMs locally for privacy.
```

### Step 3: Use Hugging Face for Retrieval
We'll use Hugging Face to create embeddings (vector representations) of your text and search for relevant chunks.

```python
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# Load a model for embeddings
model = SentenceTransformer('all-MiniLM-L6-v2')

# Load your knowledge base
with open('knowledge.txt', 'r') as f:
    documents = f.read().split('\n')  # Split into chunks

# Create embeddings
embeddings = model.encode(documents)

# Build a FAISS index for fast search
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

# Function to retrieve relevant docs
def retrieve(query, k=2):
    query_embedding = model.encode([query])
    distances, indices = index.search(query_embedding, k)
    return [documents[i] for i in indices[0]]
```

### Step 4: Use Ollama for Generation
Now, integrate Ollama to generate answers based on retrieved info.

```python
import requests

def generate_with_ollama(prompt):
    response = requests.post('http://localhost:11434/api/chat', json={
        'model': 'gemma:2b',
        'messages': [{'role': 'user', 'content': prompt}]
    })
    return response.json()['message']['content']

# Full RAG function
def rag_query(query):
    # Retrieve relevant info
    retrieved_docs = retrieve(query)
    context = '\n'.join(retrieved_docs)
    
    # Augment prompt
    prompt = f"Context: {context}\nQuestion: {query}\nAnswer:"
    
    # Generate with Ollama
    answer = generate_with_ollama(prompt)
    return answer

# Test it
print(rag_query("What is RAG?"))
```

### Step 5: Run and Test
- Save the code to `rag_system.py`.
- Run Ollama in the background: `ollama serve`.
- Execute: `python rag_system.py`.
- Ask questions like "What is Hugging Face?"—it should pull from your knowledge base.

## Hugging Face vs. Ollama: Key Differences

| Feature          | Hugging Face                          | Ollama                                |
|------------------|---------------------------------------|---------------------------------------|
| **Focus**       | Model libraries and fine-tuning      | Local model execution                |
| **Ease of Use** | Python code-heavy                    | Simple CLI/API                       |
| **Privacy**     | Can be local or cloud                | Fully local/offline                  |
| **Models**      | Thousands of open-source models      | Curated set (Llama, Gemma, etc.)     |
| **Best for RAG**| Retrieval (embeddings, search)       | Generation (answering with context)  |
| **Setup**       | `pip install transformers`           | Download binary + `ollama pull`      |

Use Hugging Face for data processing and Ollama for inference to build efficient, private RAG systems.

## Next Steps
- Experiment with larger models (e.g., `ollama pull llama3.2`).
- Add a FastAPI wrapper (like your `server.py`) to make it a web app.
- Explore advanced RAG with LangChain or LlamaIndex.

This "different" RAG approach emphasizes local, integrated tools—try it out and let me know what you build!
