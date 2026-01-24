# Prompt for Creating Notion Documentation

## 📋 Instructions

Copy the prompt below and paste it into Claude, GPT-4, or any LLM to generate comprehensive Notion documentation with diagrams for your Gen AI teaching curriculum.

---

## 🎯 THE PROMPT

```
Create comprehensive Notion documentation for a Gen AI with Python teaching curriculum. The documentation should include detailed theory explanations, visual diagrams, and examples for all four modules.

# CURRICULUM OVERVIEW

This is a 3-hour teaching curriculum that moves from Concepts → Implementation → Deployment:

## Module 1: The "Hidden" Language of LLMs (Prompt Formats) - 30 min
## Module 2: Structured Outputs using Pydantic - 30 min  
## Module 3: Running & Using LLMs - 90 min
## Module 4: Deployment with FastAPI - 30 min

---

# DOCUMENTATION REQUIREMENTS

For each module, create:

1. **Theory Section** with:
   - Clear explanations of core concepts
   - Why this topic matters
   - Real-world use cases
   - Common mistakes to avoid

2. **Visual Diagrams** including:
   - Architecture diagrams
   - Flow charts
   - Comparison tables
   - Code structure visualizations
   - Before/after examples

3. **Code Examples** with:
   - Syntax highlighting
   - Inline comments
   - Step-by-step breakdowns

4. **Hands-on Exercises**
5. **Quick Reference Cards**

---

# MODULE 1: THE "HIDDEN" LANGUAGE OF LLMs (PROMPT FORMATS)

## Theory to Explain:

### Core Concept
LLMs don't just "understand" chat - they expect specific raw string formats based on how they were trained. Using the wrong format = poor performance.

### Three Major Formats:

#### 1. Alpaca Format (Stanford)
- **Origin**: Stanford's Alpaca project (fine-tuned LLaMA 1)
- **Structure**: Explicit headers for Instruction, Input, Response
- **Use Case**: Older open-source models, simple instruction following

**Raw Format**:
```
### Instruction:
{user_instruction}

### Input:
{optional_input_data}

### Response:
```

#### 2. ChatML Format (OpenAI)
- **Origin**: OpenAI (GPT-4), adopted by Qwen
- **Structure**: Special tokens for role separation
- **Key Advantage**: Prevents prompt injection with hard token boundaries

**Raw Format**:
```
<|im_start|>system
You are a helpful assistant.<|im_end|>
<|im_start|>user
{user_message}<|im_end|>
<|im_start|>assistant
```

**Special Tokens**:
- `<|im_start|>` and `<|im_end|>` are NOT regular text
- They are special tokens in the model's vocabulary
- Token IDs: `<|im_start|>` = 100264, `<|im_end|>` = 100265
- Create HARD BOUNDARIES that prevent prompt injection

#### 3. LLaMA-2 Chat Format (Meta)
- **Origin**: Meta's LLaMA 2
- **Structure**: Complex use of [INST] tags and <<SYS>> tokens
- **Critical**: Whitespace matters! Wrong spacing = degraded quality

**Raw Format (Single-turn)**:
```
<s>[INST] <<SYS>>
You are a helpful, respectful and honest assistant.
<</SYS>>

{user_message} [/INST]
```

**Raw Format (Multi-turn)**:
```
<s>[INST] <<SYS>>
{system_message}
<</SYS>>

{user_msg_1} [/INST] {assistant_response_1} </s><s>[INST] {user_msg_2} [/INST]
```

### Diagrams Needed:
1. **Format Comparison Table** showing all three formats side-by-side
2. **Token Visualization** showing how special tokens work
3. **Prompt Injection Prevention** diagram for ChatML
4. **Whitespace Sensitivity** diagram for LLaMA-2
5. **When to Use Which Format** decision tree

---

# MODULE 2: STRUCTURED OUTPUTS USING PYDANTIC

## Theory to Explain:

### The Problem
LLMs return strings. Even with JSON mode, you get:
- Strings that might not be valid JSON
- No type information
- No validation
- Manual parsing required

**Example of the problem**:
```python
response = "Here is your JSON: {\"name\": \"John\", \"age\": 30}"
# This breaks json.loads() because of the extra text!
```

### The Solution: Pydantic + Instructor

**Instructor** is the industry-standard library that:
- Patches OpenAI's client to add `response_model` parameter
- Automatically validates LLM outputs against Pydantic models
- Retries if output doesn't match schema
- Returns typed Python objects instead of strings

**How it works**:
```python
import instructor
from openai import OpenAI
from pydantic import BaseModel

# 1. Define the desired structure
class UserInfo(BaseModel):
    name: str
    age: int
    is_developer: bool

# 2. Patch the client (enables "response_model")
client = instructor.from_openai(OpenAI())

# 3. Call the model with response_model
user = client.chat.completions.create(
    model="gpt-3.5-turbo",
    response_model=UserInfo,  # <--- THE MAGIC!
    messages=[{"role": "user", "content": "John is a 25 year old python coder."}]
)

# 4. Get typed object
print(user.name)  # Output: John (Typed as string)
print(user.is_developer)  # Output: True (Typed as boolean)
```

### Diagrams Needed:
1. **Before/After Comparison** showing manual parsing vs instructor
2. **Instructor Flow Diagram** showing how it works under the hood
3. **Pydantic Model Structure** visualization
4. **Type Safety Benefits** diagram
5. **Validation Flow** showing retry mechanism

---

# MODULE 3: RUNNING & USING LLMs

## Theory to Explain:

### 1. Cloud APIs (OpenAI & Gemini)

**OpenAI**:
```python
from openai import OpenAI
client = OpenAI(api_key="sk-...")
response = client.chat.completions.create(...)
```

**Gemini**:
```python
import google.generativeai as genai
genai.configure(api_key="AIza...")
model = genai.GenerativeModel('gemini-pro')
response = model.generate_content("Hello world")
```

### 2. Running Locally with Ollama

**Key Concept**: Ollama is like Docker for LLMs

**The Docker Command**:
```bash
docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
```

**Pulling a Model**:
```bash
docker exec -it ollama ollama run llama3
```

**Critical Insight**: Ollama provides an OpenAI-compatible endpoint!
```python
client = OpenAI(
    base_url='http://localhost:11434/v1',
    api_key='ollama',  # required but unused
)
# Same code works for both OpenAI and Ollama!
```

### 3. Base vs Instruction-Tuned Models

**Base Model** (Autocomplete engine):
- Input: "The capital of France is"
- Output: " a beautiful city."

**Instruction-Tuned Model** (Chatbot):
- Input: "The capital of France is"
- Output: "Paris."

### Diagrams Needed:
1. **Cloud vs Local Comparison** table
2. **Ollama Architecture** diagram
3. **OpenAI-Compatible Endpoint** visualization
4. **Base vs Instruction-Tuned** comparison
5. **Docker Setup Flow** diagram
6. **Model Selection Decision Tree**

---

# MODULE 4: DEPLOYMENT WITH FASTAPI

## Theory to Explain:

### The Critical Concept: Blocking vs Non-Blocking

**The Problem with Synchronous Code**:
```python
@app.post("/chat")
def chat(prompt: str):  # ❌ BLOCKING!
    response = client.chat.completions.create(...)
    return response
```

**What happens**:
1. Server makes API call to OpenAI
2. Waits 2-10 seconds for response
3. During this time, server is BLOCKED
4. No other requests can be processed!

**Result**: One user at a time = terrible performance

**The Solution: Async/Await**:
```python
@app.post("/chat")
async def chat(prompt: str):  # ✅ NON-BLOCKING!
    response = await client.chat.completions.create(...)
    return response
```

**What happens**:
1. Server makes API call to OpenAI
2. While waiting, server can handle OTHER requests
3. When response arrives, server resumes this request

**Result**: Multiple users served concurrently!

### Restaurant Analogy

**Synchronous (Bad)**:
- Waiter takes order from Table 1
- Waits in kitchen until food is ready
- Brings food to Table 1
- Only then takes order from Table 2

**Asynchronous (Good)**:
- Waiter takes order from Table 1
- While kitchen cooks, takes order from Table 2
- When food ready, brings to Table 1
- Continues serving multiple tables

### Streaming Responses

Instead of:
```
[wait 10 seconds] "Here is your complete answer..."
```

User sees:
```
"Here" [0.1s] "is" [0.1s] "your" [0.1s] "complete" [0.1s] "answer"
```

**Implementation**:
```python
async def generate_response(prompt: str):
    stream = await client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        stream=True  # Enable streaming
    )
    async for chunk in stream:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content

@app.post("/chat")
async def chat_endpoint(prompt: str):
    return StreamingResponse(generate_response(prompt), media_type="text/plain")
```

### Diagrams Needed:
1. **Blocking vs Non-Blocking** comparison diagram
2. **Restaurant Analogy** visualization
3. **Async/Await Flow** diagram
4. **Streaming Response** timeline
5. **FastAPI Architecture** diagram
6. **Production Deployment** checklist

---

# FORMATTING GUIDELINES FOR NOTION

1. **Use Notion's Built-in Features**:
   - Toggle blocks for expandable sections
   - Callout blocks for important notes
   - Code blocks with syntax highlighting
   - Tables for comparisons
   - Dividers between sections

2. **Visual Hierarchy**:
   - H1 for module titles
   - H2 for main sections
   - H3 for subsections
   - Bullet points for lists
   - Numbered lists for steps

3. **Color Coding**:
   - 🔴 Red: Critical warnings
   - 🟡 Yellow: Important notes
   - 🟢 Green: Best practices
   - 🔵 Blue: Examples
   - 🟣 Purple: Advanced topics

4. **Diagram Styles**:
   - Use Mermaid syntax for flowcharts
   - ASCII art for simple diagrams
   - Tables for comparisons
   - Emoji for visual markers

5. **Code Blocks**:
   - Always specify language for syntax highlighting
   - Add comments explaining key lines
   - Show before/after examples

---

# OUTPUT FORMAT

Please create the documentation in Notion-compatible markdown format with:

1. **Table of Contents** at the top
2. **Module 1** with all theory, diagrams, and examples
3. **Module 2** with all theory, diagrams, and examples
4. **Module 3** with all theory, diagrams, and examples
5. **Module 4** with all theory, diagrams, and examples
6. **Quick Reference Cards** for each module
7. **Glossary** of terms
8. **Additional Resources** section

Make it comprehensive, visual, and easy to understand for students learning Gen AI for the first time.
```

---

## 📝 How to Use This Prompt

1. **Copy the entire prompt** above (everything in the code block)
2. **Paste into Claude, GPT-4, or your preferred LLM**
3. **Wait for the comprehensive documentation** to be generated
4. **Copy the output** and paste into Notion
5. **Format** using Notion's features (add colors, toggles, etc.)

---

## 💡 Tips for Best Results

- Use **Claude 3.5 Sonnet** or **GPT-4** for best diagram generation
- Ask for **Mermaid diagrams** if you want flowcharts
- Request **ASCII art** for simple visualizations
- Ask to **expand specific sections** if you need more detail
- Request **additional examples** for any concept

---

## 🎨 Notion Formatting Tips

After pasting the generated content:

1. **Add Toggles** for expandable sections
2. **Use Callouts** for important notes
3. **Add Colors** to code blocks and headers
4. **Create Databases** for exercises and examples
5. **Add Icons** to section headers
6. **Use Columns** for side-by-side comparisons

---

## 📊 Example Diagrams to Request

You can also ask the LLM to create specific diagrams:

```
"Create a Mermaid flowchart showing the decision tree for choosing between Alpaca, ChatML, and LLaMA-2 formats"

"Create an ASCII diagram showing how ChatML special tokens prevent prompt injection"

"Create a comparison table showing OpenAI vs Gemini vs Ollama features"

"Create a sequence diagram showing async/await flow in FastAPI"
```

---

**Ready to generate your Notion docs!** 🚀
