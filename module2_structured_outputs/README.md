# Module 2: Structured Outputs using Pydantic

## 🎯 Goal
Move beyond parsing messy strings. Teach how to force an LLM to speak "Code" (JSON) instead of "English."

---

## ❌ The Problem

LLMs return **strings**. If you ask for JSON, they might return:

```
Here is your JSON: {"key": "value"}
```

This **breaks code parsers** because of the extra text!

---

## ✅ The Solution: Pydantic + Instructor

While you can do this manually with prompts, the **`instructor`** library (patched onto OpenAI/Pydantic) is the **industry standard** for teaching this.

### What is Instructor?

`instructor` is a library that:
- Patches OpenAI's client to add `response_model` parameter
- Automatically validates LLM outputs against Pydantic models
- Retries if the output doesn't match the schema
- Returns typed Python objects instead of strings

---

## 🔑 Key Concepts

### 1. Pydantic Models
Define the structure you want:

```python
from pydantic import BaseModel

class UserInfo(BaseModel):
    name: str
    age: int
    is_developer: bool
```

### 2. Instructor Patching
Patch the OpenAI client:

```python
import instructor
from openai import OpenAI

client = instructor.from_openai(OpenAI())
```

### 3. Type-Safe Responses
Get Python objects, not strings:

```python
user = client.chat.completions.create(
    model="gpt-4o-mini",
    response_model=UserInfo,  # <--- The Magic!
    messages=[...]
)

print(user.name)  # Typed as string
print(user.age)   # Typed as int
```

---

## 📁 Files in This Module

1. **`basic_instructor.py`** - Introduction to instructor
2. **`advanced_validation.py`** - Complex models and validation
3. **`real_world_examples.py`** - Practical use cases
4. **`INSTRUCTOR_GUIDE.md`** - Detailed documentation

---

## 🚀 Quick Start

```bash
# Install instructor
pip install instructor

# Run basic example
python basic_instructor.py

# Run advanced examples
python advanced_validation.py

# See real-world use cases
python real_world_examples.py
```

---

## 🎓 Learning Objectives

By the end of this module, you will:

- ✅ Understand why string parsing is problematic
- ✅ Use Pydantic to define data structures
- ✅ Patch OpenAI client with instructor
- ✅ Get type-safe, validated responses
- ✅ Handle complex nested structures
- ✅ Implement retry logic for validation

---

## 💡 Why This Matters

### Without Instructor (Manual Parsing)
```python
response = client.chat.completions.create(...)
text = response.choices[0].message.content

# Hope it's valid JSON...
data = json.loads(text)  # Might fail!

# Hope it has the right fields...
name = data["name"]  # Might not exist!
```

### With Instructor (Type-Safe)
```python
user = client.chat.completions.create(
    response_model=UserInfo,
    ...
)

# Guaranteed to have these fields!
print(user.name)  # Always a string
print(user.age)   # Always an int
```

---

## 📊 Comparison

| Approach | Type Safety | Validation | Retries | Ease of Use |
|----------|-------------|------------|---------|-------------|
| **Manual JSON** | ❌ No | ❌ No | ❌ No | ❌ Hard |
| **JSON Mode** | ❌ No | ⚠️ Partial | ❌ No | ⚠️ Medium |
| **Instructor** | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Easy |

---

## 🔧 Installation

```bash
pip install instructor openai pydantic
```

---

## 🎯 Next Module

Once you master structured outputs, move to **Module 3: Running & Using LLMs** to learn about different deployment options!

---

**Duration**: 30 minutes  
**Difficulty**: Intermediate  
**Prerequisites**: Basic Python, Module 1 completed
