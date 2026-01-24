# Code Comments Guide

## 📚 Overview

All Python files in this teaching curriculum now include comprehensive inline comments to help students understand every step of the code.

---

## 🎯 Commenting Philosophy

### **For Teaching Code**

Teaching code should be **over-commented** rather than under-commented. Every line that might be unclear to a beginner should have an explanation.

### **Three Levels of Comments**

1. **Module-Level** - What the file does and why
2. **Function-Level** - What the function does, parameters, returns
3. **Inline** - What each line or block does

---

## ✅ What's Been Enhanced

### **Module 1: Prompt Formats**

#### **`alpaca_format.py`**
✅ Enhanced function docstring with:
- Clear explanation of Alpaca format structure
- Parameter examples
- Return value description
- Usage example

✅ Added inline comments explaining:
- Why headers must be exact (`### Instruction:`)
- What `\n\n` does (creates blank lines)
- When to use optional parameters
- How `repr()` shows raw strings
- What each API parameter does

#### **`chatml_format.py`**
✅ Comments explain:
- Special tokens vs regular text
- Token IDs (100264, 100265)
- Security advantages
- Role separation

#### **`llama2_format.py`**
✅ Comments emphasize:
- Whitespace sensitivity
- System message rules
- Multi-turn structure
- Common mistakes

---

## 📝 Comment Style Guide

### **1. Module Docstring**
```python
"""
Module 1: Alpaca Prompt Format
===============================
The "Hidden" Language of LLMs - Part 1

Goal: Understand that LLMs don't just "understand" chat - they expect
specific raw string formats based on how they were trained.

Alpaca Format Origin: Stanford's Alpaca model (fine-tuned LLaMA 1)
Use Case: Older open-source models, simple instruction following
"""
```

### **2. Function Docstring**
```python
def create_alpaca_prompt(instruction: str, input_data: str = "", response_prefix: str = "") -> str:
    """
    Create a prompt in Alpaca format.
    
    This is the RAW STRING the model actually sees!
    
    Alpaca format has three parts:
    1. ### Instruction: - What task to perform
    2. ### Input: - Optional context/data (can be omitted)
    3. ### Response: - Where the model generates its answer
    
    Args:
        instruction: The task instruction (e.g., "Translate to Spanish")
        input_data: Optional context/data for the task (e.g., "Hello world")
        response_prefix: Optional start of the response (rarely used)
    
    Returns:
        Formatted Alpaca prompt string with proper headers and newlines
    
    Example:
        >>> create_alpaca_prompt("Summarize this", "AI is transforming...")
        '### Instruction:\\nSummarize this\\n\\n### Input:\\nAI is transforming...\\n\\n### Response:\\n'
    """
```

### **3. Inline Comments**
```python
# Start with the Instruction header
# Note: Must be exactly "### Instruction:" with capital I and colon
prompt = "### Instruction:\n"

# Add the actual instruction text
# \n\n creates a blank line after the instruction for readability
prompt += f"{instruction}\n\n"
```

### **4. Section Headers**
```python
# ============================================================================
# Example 1: Simple Instruction (No Input)
# ============================================================================
# This example shows the simplest form of Alpaca format:
# Just an instruction, no input data needed
```

### **5. Explanatory Comments**
```python
# repr() shows the string with visible \n characters
# This helps you see the exact format including newlines
print(repr(alpaca_prompt1))
```

---

## 🎓 Teaching-Specific Comments

### **Why Comments**
Explain WHY something is done, not just WHAT:

```python
# ✅ GOOD:
# Use repr() to show \n characters because students need to see
# the exact format the model receives, including newlines
print(repr(prompt))

# ❌ BAD:
# Print the prompt
print(repr(prompt))
```

### **Common Pitfalls**
Highlight common mistakes:

```python
# CRITICAL: Must be exactly "### Instruction:" with capital I
# Wrong: "### instruction:" or "##Instruction:" or "Instruction:"
prompt = "### Instruction:\n"
```

### **Parameter Explanations**
Explain what parameters do in context:

```python
response = client.chat.completions.create(
    model="gpt-4o-mini",  # The model to use
    messages=[{"role": "user", "content": alpaca_prompt1}],  # Our Alpaca-formatted prompt
    temperature=0.7  # Controls randomness (0.7 = balanced creativity)
)
```

---

## 📊 Files with Enhanced Comments

| File | Module | Status |
|------|--------|--------|
| `alpaca_format.py` | Module 1 | ✅ Enhanced |
| `chatml_format.py` | Module 1 | ✅ Good comments |
| `llama2_format.py` | Module 1 | ✅ Good comments |
| `basic_instructor.py` | Module 2 | ✅ Good comments |
| `ollama_local.py` | Module 3 | ✅ Good comments |
| `async_streaming.py` | Module 4 | ✅ Excellent comments |

---

## 💡 Best Practices for Teaching Code

### **1. Assume Zero Knowledge**
Comment as if the student has never seen this before.

### **2. Explain Jargon**
```python
# API (Application Programming Interface) - a way to communicate with a service
client = OpenAI(api_key=...)
```

### **3. Show Examples**
```python
# Example: create_alpaca_prompt("Translate to Spanish", "Hello")
# Returns: '### Instruction:\nTranslate to Spanish\n\n### Input:\nHello\n\n### Response:\n'
```

### **4. Highlight Important Concepts**
```python
# IMPORTANT: This is the RAW STRING the model sees!
# Not a JSON object, not a chat interface - just this exact text
```

### **5. Link to Documentation**
```python
# For more on temperature, see: https://platform.openai.com/docs/api-reference/chat/create#temperature
temperature=0.7
```

---

## 🔍 How to Read the Comments

### **For Students**

1. **Read module docstring first** - Understand the big picture
2. **Read function docstrings** - Know what each function does
3. **Follow inline comments** - Understand each step
4. **Try modifying** - Change values and see what happens

### **For Teachers**

1. **Use comments as lecture notes** - They explain key concepts
2. **Point out specific comments** - During live coding
3. **Ask students to add comments** - As an exercise
4. **Review comment quality** - When students submit code

---

## 📝 Comment Checklist

When writing teaching code, ensure:

- [ ] Module docstring explains the purpose
- [ ] Function docstrings include Args, Returns, Examples
- [ ] Complex logic has explanatory comments
- [ ] Magic numbers are explained
- [ ] Common mistakes are highlighted
- [ ] API parameters are documented
- [ ] Jargon is defined
- [ ] Examples are provided
- [ ] Links to resources are included
- [ ] WHY is explained, not just WHAT

---

## 🎯 Examples of Good vs Bad Comments

### **Example 1: Variable Assignment**

```python
# ❌ BAD:
# Set instruction
instruction = "Translate to Spanish"

# ✅ GOOD:
# Define the task we want the model to perform
# This will be wrapped in Alpaca format's ### Instruction: header
instruction = "Translate to Spanish"
```

### **Example 2: Function Call**

```python
# ❌ BAD:
# Create prompt
prompt = create_alpaca_prompt(instruction)

# ✅ GOOD:
# Create the Alpaca-formatted prompt
# This wraps our instruction in the proper ### Instruction: / ### Response: format
prompt = create_alpaca_prompt(instruction)
```

### **Example 3: API Call**

```python
# ❌ BAD:
# Call API
response = client.chat.completions.create(...)

# ✅ GOOD:
# Send the formatted prompt to OpenAI's API
# The model will process our Alpaca-formatted string and generate a response
response = client.chat.completions.create(
    model="gpt-4o-mini",  # Using the mini model for cost efficiency
    messages=[{"role": "user", "content": alpaca_prompt1}],  # Our formatted prompt
    temperature=0.7  # Balanced creativity (0=deterministic, 1=creative)
)
```

---

## 🚀 Next Steps

### **For Continued Improvement**

1. **Student Feedback**: Ask students which parts are unclear
2. **Add More Examples**: In docstrings and comments
3. **Visual Aids**: Add ASCII diagrams in comments where helpful
4. **Interactive Comments**: Suggest modifications students can try
5. **Error Explanations**: Comment common error messages

---

## 📖 Resources

- [PEP 257 - Docstring Conventions](https://peps.python.org/pep-0257/)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
- [Writing Great Documentation](https://www.writethedocs.org/)

---

**Last Updated**: January 2026  
**Status**: All teaching files have comprehensive comments  
**Philosophy**: Over-comment for teaching, under-comment for production
