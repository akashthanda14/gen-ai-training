# 🎓 Gen AI with Python - Organized Teaching Curriculum

**A complete, modular teaching curriculum from Concepts → Implementation → Deployment**

---

## 📁 **Clean Folder Structure**

```
prompts/
│
├── 📚 module1_prompt_formats/          # 30 min - The "Hidden" Language
│   ├── README.md                       # Module overview & learning objectives
│   ├── alpaca_format.py                # Stanford's Alpaca format
│   ├── chatml_format.py                # OpenAI's ChatML format
│   ├── llama2_format.py                # Meta's LLaMA-2 format
│   ├── 07_alpaca_format.py             # (Legacy - same content)
│   ├── 08_chatml_format.py             # (Legacy - same content)
│   ├── 09_llama2_format.py             # (Legacy - same content)
│   └── docs/                           # Additional documentation
│
├── 📦 module2_structured_outputs/      # 30 min - Pydantic + Instructor
│   ├── README.md                       # Module overview
│   ├── basic_instructor.py             # Industry-standard instructor library
│   ├── 10_pydantic_structured_outputs.py  # (Legacy version)
│   └── docs/                           # Additional documentation
│
├── 🚀 module3_running_llms/            # 90 min - Cloud & Local Models
│   ├── README.md                       # Module overview
│   ├── ollama_local.py                 # Ollama: Docker for LLMs
│   ├── 11_openai_advanced.py           # OpenAI advanced features
│   ├── 12_gemini_advanced.py           # Gemini API features
│   ├── 13_ollama_local.py              # (Legacy - same as ollama_local.py)
│   ├── 15_huggingface_models.py        # Hugging Face transformers
│   └── docs/
│       └── 14_ollama_docker_setup.md   # Docker deployment guide
│
├── ⚡ module4_deployment/              # 30 min - FastAPI Production
│   ├── README.md                       # Module overview
│   ├── async_streaming.py              # Async/await & streaming
│   ├── 16_fastapi_llm_endpoint.py      # (Legacy - full production server)
│   └── docs/                           # Additional documentation
│
├── 📖 docs/                            # General documentation
│   ├── LLM_LECTURE_GUIDE.md            # Original comprehensive guide
│   ├── LECTURE_STEPS.md                # Step-by-step instructions
│   ├── QUICK_REFERENCE_LECTURE.md      # Quick reference card
│   ├── LECTURE_SUMMARY.md              # Complete overview
│   └── ... (other docs)
│
├── 🗂️ old_examples/                    # Original basic examples
│   ├── 01_hello_world.py
│   ├── 02_zero_shot_prompting.py
│   ├── 03_few_shot_prompting.py
│   └── ... (other basic examples)
│
├── 📋 TEACHING_CURRICULUM.md           # Master teaching guide
├── 📋 IMPLEMENTATION_COMPLETE.md       # Implementation summary
├── 📋 README.md                        # Original project README
├── 📋 requirements.txt                 # All dependencies
├── 🔧 .env                             # API keys (configure this)
└── 🔧 .env.example                     # Example environment file
```

---

## 🎯 **Quick Start Guide**

### **1. Install Dependencies**
```bash
cd /Users/work/Desktop/LLM/GEN-AI/prompts
pip install -r requirements.txt
```

### **2. Configure API Keys**
```bash
# Copy example and edit
cp .env.example .env

# Add your keys
OPENAI_API_KEY=sk-...
GEMINI_API_KEY=AI...
```

### **3. Start Teaching!**

#### **Module 1: Prompt Formats (30 min)**
```bash
cd module1_prompt_formats

# Read the overview
cat README.md

# Run examples
python alpaca_format.py
python chatml_format.py
python llama2_format.py
```

#### **Module 2: Structured Outputs (30 min)**
```bash
cd ../module2_structured_outputs

# Read the overview
cat README.md

# Run instructor example
python basic_instructor.py
```

#### **Module 3: Running LLMs (90 min)**
```bash
cd ../module3_running_llms

# Read the overview
cat README.md

# Set up Ollama first
brew install ollama      # macOS
ollama serve            # Start server
ollama pull llama3      # Pull model

# Run examples
python ollama_local.py
python 11_openai_advanced.py
python 12_gemini_advanced.py
python 15_huggingface_models.py
```

#### **Module 4: Deployment (30 min)**
```bash
cd ../module4_deployment

# Read the overview
cat README.md

# Run FastAPI server
python async_streaming.py

# Access docs
open http://localhost:8000/docs
```

---

## 📚 **Module Breakdown**

### **Module 1: The "Hidden" Language of LLMs**
**Goal**: Teach that LLMs expect specific raw string formats

**Files**:
- `alpaca_format.py` - Stanford's format with `### Instruction:`
- `chatml_format.py` - OpenAI's format with `<|im_start|>`
- `llama2_format.py` - Meta's format with `<s>[INST]`

**Key Insight**: Different models = different languages!

---

### **Module 2: Structured Outputs using Pydantic**
**Goal**: Move from strings to typed Python objects

**Files**:
- `basic_instructor.py` - Industry-standard `instructor` library

**Key Insight**: `response_model=UserInfo` gives typed objects!

---

### **Module 3: Running & Using LLMs**
**Goal**: Learn cloud APIs, local models, and Hugging Face

**Files**:
- `ollama_local.py` - Ollama: Docker for LLMs
- `11_openai_advanced.py` - OpenAI advanced features
- `12_gemini_advanced.py` - Gemini API
- `15_huggingface_models.py` - Transformers library
- `docs/14_ollama_docker_setup.md` - Docker guide

**Key Insight**: Ollama provides OpenAI-compatible endpoints!

---

### **Module 4: Deployment with FastAPI**
**Goal**: Build production APIs with async/await

**Files**:
- `async_streaming.py` - Async/await & streaming responses
- `16_fastapi_llm_endpoint.py` - Full production server

**Key Insight**: `def` = blocking, `async def` = concurrent!

---

## 🎓 **Teaching Flow**

```
1. Module 1 (30 min)
   ↓ Show raw strings with repr()
   ↓ Compare all three formats
   
2. Module 2 (30 min)
   ↓ Show string parsing problem
   ↓ Introduce instructor solution
   
3. Module 3 (90 min)
   ↓ Demo Ollama's ease
   ↓ Show OpenAI-compatible endpoint
   
4. Module 4 (30 min)
   ↓ Two terminals: sync vs async
   ↓ Show streaming word-by-word
   
🎉 Ready to build production LLM apps!
```

---

## 📊 **Tools Summary**

| Task | Tool | Why? |
|------|------|------|
| **Prompting** | Raw Strings | Understand what model sees |
| **Structure** | instructor | Modern, Pythonic outputs |
| **Local Run** | Ollama | Easiest zero-setup inference |
| **Deployment** | FastAPI | Native async for LLM latency |

---

## 🗂️ **File Organization**

### **Active Teaching Files** (Use these!)
- `module1_prompt_formats/*.py` - New, well-organized
- `module2_structured_outputs/*.py` - New, with instructor
- `module3_running_llms/*.py` - New, comprehensive
- `module4_deployment/*.py` - New, production-ready

### **Legacy Files** (Backup/Reference)
- `module*/0*_*.py` - Original numbered files (moved into modules)
- `old_examples/` - Original basic examples

### **Documentation**
- Each module has its own `README.md`
- `docs/` folder has comprehensive guides
- `TEACHING_CURRICULUM.md` - Master guide

---

## ✅ **What's Included**

### **Python Files**: 15 total
- Module 1: 6 files (3 new + 3 legacy)
- Module 2: 2 files (1 new + 1 legacy)
- Module 3: 5 files (1 new + 4 legacy)
- Module 4: 2 files (1 new + 1 legacy)

### **Documentation**: 10+ files
- 4 Module READMEs
- 5+ General guides
- 1 Docker setup guide

### **All Files Include**:
- ✅ Detailed teaching points
- ✅ Code comments
- ✅ Error handling
- ✅ Real-world examples
- ✅ Before/after comparisons

---

## 🎯 **Learning Outcomes**

After completing all modules, students will:

✅ Understand why prompt formats exist  
✅ Use instructor for type-safe outputs  
✅ Run models locally with Ollama  
✅ Deploy production APIs with async/await  
✅ Build real-world LLM applications  

---

## 📝 **Next Steps**

1. **Review** each module's README
2. **Test** all Python files
3. **Customize** for your audience
4. **Practice** demonstrations
5. **Teach** with confidence!

---

## 🚀 **Start Teaching**

```bash
cd module1_prompt_formats
python alpaca_format.py
```

**Total Duration**: ~3 hours  
**Modules**: 4  
**Status**: ✅ Fully Organized & Ready!

---

**Happy Teaching! 🎓🚀**
