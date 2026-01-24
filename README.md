# Prompt Engineering Tutorial

A comprehensive guide to teaching prompt engineering techniques using practical Python examples with OpenAI and Google Gemini APIs.

---

## 📚 Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Setup Instructions](#setup-instructions)
4. [Prompting Techniques](#prompting-techniques)
5. [Running the Examples](#running-the-examples)
6. [Teaching Guide](#teaching-guide)
7. [Troubleshooting](#troubleshooting)

---

## 🎯 Overview

This repository contains **6 progressive examples** that teach fundamental prompt engineering techniques:

| File | Technique | Difficulty | Key Learning |
|------|-----------|------------|--------------|
| `01_hello_world.py` | Basic API Call | Beginner | Understanding LLM API structure |
| `02_zero_shot_prompting.py` | Zero-Shot | Beginner | Direct instructions without examples |
| `03_few_shot_prompting.py` | Few-Shot | Intermediate | Learning from examples |
| `04_chain_of_thought.py` | Chain-of-Thought | Intermediate | Step-by-step reasoning |
| `05_persona_based_prompting.py` | Persona-Based | Intermediate | Creating AI characters |
| `06_gemini_example.py` | Alternative API | Beginner | Using different LLM providers |

---

## ✅ Prerequisites

### Required Knowledge
- Basic Python programming
- Understanding of APIs
- Command line basics

### Required Accounts
1. **OpenAI Account** - Get API key from [OpenAI Platform](https://platform.openai.com/api-keys)
2. **Google AI Account** (optional) - Get API key from [Google AI Studio](https://ai.google.dev/)

### System Requirements
- Python 3.8 or higher
- pip (Python package manager)
- Text editor or IDE

---

## 🚀 Setup Instructions

### Step 1: Clone or Download
Download this repository to your local machine.

### Step 2: Install Dependencies
```bash
# Navigate to the project directory
cd /path/to/prompts

# Install required packages
pip install -r requirements.txt
```

### Step 3: Configure API Keys
Create a `.env` file in the project root:

```bash
# Create .env file
touch .env
```

Add your API keys to `.env`:
```env
# OpenAI API Key (Required for examples 1-5)
OPENAI_API_KEY=your_openai_api_key_here

# Optional: Specify OpenAI model (default: gpt-4o-mini)
OPENAI_MODEL=gpt-4o-mini

# Google Gemini API Key (Required only for example 6)
GEMINI_API_KEY=your_gemini_api_key_here
```

**⚠️ IMPORTANT:** Never commit your `.env` file to version control!

### Step 4: Verify Setup
Test your setup with the hello world example:
```bash
python 01_hello_world.py
```

If you see a response, you're ready to go! 🎉

---

## 📖 Prompting Techniques

### 1️⃣ Hello World - Basic API Call
**File:** `01_hello_world.py`

**What it teaches:**
- How to initialize an LLM client
- Structure of API requests
- Role of system vs user messages
- Getting and displaying responses

**Key Concepts:**
```python
# System message: Defines AI behavior
{"role": "system", "content": "You are a helpful assistant"}

# User message: The actual query
{"role": "user", "content": "What is 2+2?"}
```

**When to use:** Every LLM interaction starts here!

---

### 2️⃣ Zero-Shot Prompting
**File:** `02_zero_shot_prompting.py`

**What it teaches:**
- Giving instructions without examples
- Relying on model's pre-trained knowledge
- Clear, direct prompting

**Example:**
```
Instruction: "Answer only coding questions. Refuse everything else."
Query: "Explain Python"
Result: Model answers because it's coding-related
```

**When to use:**
- Simple, straightforward tasks
- When you don't have examples
- Quick one-off queries

**Pros:** Fast, simple
**Cons:** Less control over output format

---

### 3️⃣ Few-Shot Prompting
**File:** `03_few_shot_prompting.py`

**What it teaches:**
- Teaching by example
- Consistent output formatting
- Pattern recognition

**Example:**
```
Examples:
Q: "What's 2+2?" → A: {"answer": 4, "type": "math"}
Q: "Hi there" → A: {"answer": null, "type": "greeting"}

New Query: "What's 5+5?"
Result: {"answer": 10, "type": "math"}
```

**When to use:**
- Need specific output format (JSON, CSV, etc.)
- Task requires particular style
- Zero-shot gives inconsistent results

**Pros:** Better format control, more consistent
**Cons:** Uses more tokens, requires good examples

---

### 4️⃣ Chain-of-Thought (CoT) Prompting
**File:** `04_chain_of_thought.py`

**What it teaches:**
- Breaking down complex problems
- Step-by-step reasoning
- Improving accuracy on hard tasks

**Example:**
```
Problem: "Solve 2 + 3 × 5 ÷ 10"

Without CoT: "3.5" (might be wrong)

With CoT:
Step 1: Multiply 3 × 5 = 15
Step 2: Divide 15 ÷ 10 = 1.5
Step 3: Add 2 + 1.5 = 3.5
Answer: 3.5 ✓
```

**When to use:**
- Complex math or logic problems
- Multi-step reasoning required
- Need to verify the logic
- Debugging code or processes

**Pros:** Higher accuracy, transparent reasoning
**Cons:** More tokens, slower responses

---

### 5️⃣ Persona-Based Prompting
**File:** `05_persona_based_prompting.py`

**What it teaches:**
- Creating AI characters
- Consistent personality and style
- Context-aware responses

**Example:**
```
Persona: "Friendly college student who speaks Punjabi-English"

Q: "Coming to class?"
A: "Haan pra, aana hi paina 😂"

Q: "How was exam?"
A: "Thik-thak hoya, kujh tough si 😎"
```

**When to use:**
- Chatbots with personality
- Brand voice consistency
- Educational tutors
- Entertainment/gaming

**Pros:** Engaging, consistent character
**Cons:** Requires detailed persona definition

---

### 6️⃣ Using Different LLM Providers
**File:** `06_gemini_example.py`

**What it teaches:**
- LLM providers have different APIs
- Same prompting principles apply everywhere
- How to switch between providers

**Comparison:**
```python
# OpenAI
client = OpenAI(api_key=key)
response = client.chat.completions.create(...)

# Google Gemini
client = genai.Client(api_key=key)
response = client.models.generate_content(...)
```

**When to use:**
- Comparing model performance
- Cost optimization
- Specific model features

---

## 🏃 Running the Examples

### Run Individual Examples
```bash
# Example 1: Hello World
python 01_hello_world.py

# Example 2: Zero-Shot
python 02_zero_shot_prompting.py

# Example 3: Few-Shot
python 03_few_shot_prompting.py

# Example 4: Chain-of-Thought
python 04_chain_of_thought.py

# Example 5: Persona (Interactive)
python 05_persona_based_prompting.py

# Example 6: Gemini (requires GEMINI_API_KEY)
python 06_gemini_example.py
```

### Modify Examples
Each file is self-contained. To experiment:

1. Open the file in your editor
2. Find the `USER_PROMPT` variable
3. Change the question/instruction
4. Run the file again

**Example:**
```python
# In 02_zero_shot_prompting.py
USER_PROMPT = "Explain loops in Python"  # Change this!
```

---

## 👨‍🏫 Teaching Guide

### Recommended Teaching Order

#### Session 1: Foundations (30 minutes)
1. **Explain LLMs basics** (10 min)
   - What are LLMs?
   - How do they work?
   - API vs ChatGPT interface

2. **Run Example 1** (10 min)
   - Show the code structure
   - Explain system vs user roles
   - Demonstrate live API call

3. **Hands-on Exercise** (10 min)
   - Students modify the prompt
   - Try different questions
   - Observe different responses

#### Session 2: Zero-Shot vs Few-Shot (45 minutes)
1. **Zero-Shot Prompting** (15 min)
   - Run Example 2
   - Explain when it works well
   - Show limitations

2. **Few-Shot Prompting** (15 min)
   - Run Example 3
   - Compare with zero-shot
   - Demonstrate format control

3. **Exercise** (15 min)
   - Create a sentiment analyzer
   - Try both techniques
   - Compare results

#### Session 3: Advanced Techniques (45 minutes)
1. **Chain-of-Thought** (20 min)
   - Run Example 4
   - Solve a math problem together
   - Show reasoning transparency

2. **Persona-Based** (15 min)
   - Run Example 5
   - Create a custom persona
   - Test consistency

3. **Different Providers** (10 min)
   - Run Example 6
   - Compare APIs
   - Discuss trade-offs

### Teaching Tips

✅ **DO:**
- Start simple, build complexity
- Let students experiment
- Show real-world use cases
- Encourage questions
- Compare different approaches

❌ **DON'T:**
- Overwhelm with theory
- Skip hands-on practice
- Assume prior knowledge
- Rush through examples

### Discussion Questions

1. **When would you use zero-shot vs few-shot?**
   - Answer: Zero-shot for simple tasks, few-shot for format control

2. **Why is chain-of-thought better for math?**
   - Answer: Shows reasoning, catches errors, more accurate

3. **How do you create a good persona?**
   - Answer: Clear personality, consistent examples, specific traits

4. **What are the trade-offs of different LLM providers?**
   - Answer: Cost, speed, capabilities, API design

### Hands-On Exercises

#### Exercise 1: Build a Code Reviewer
```
Task: Create a prompt that reviews code and returns JSON
Technique: Few-shot prompting
Format: {"issues": [], "score": 0-10, "suggestions": []}
```

#### Exercise 2: Math Tutor
```
Task: Solve word problems with step-by-step explanations
Technique: Chain-of-thought
Example: "If John has 5 apples and buys 3 more..."
```

#### Exercise 3: Customer Support Bot
```
Task: Create a helpful, friendly support persona
Technique: Persona-based
Personality: Professional but warm, patient, solution-focused
```

---

## 🔧 Troubleshooting

### Common Issues

#### 1. API Key Not Found
```
Error: OPENAI_API_KEY is not set
```
**Solution:**
- Check `.env` file exists
- Verify key is correct
- No spaces around `=` in `.env`
- Restart terminal after creating `.env`

#### 2. Module Not Found
```
Error: No module named 'openai'
```
**Solution:**
```bash
pip install -r requirements.txt
```

#### 3. Rate Limit Error
```
Error: Rate limit exceeded
```
**Solution:**
- Wait a few seconds
- Check your API usage quota
- Upgrade your API plan if needed

#### 4. Invalid API Key
```
Error: Incorrect API key provided
```
**Solution:**
- Regenerate key from OpenAI dashboard
- Copy the entire key (starts with `sk-`)
- Update `.env` file

#### 5. Gemini Example Not Working
```
Error: GEMINI_API_KEY is not set
```
**Solution:**
- Get key from https://ai.google.dev/
- Add to `.env` file
- Only needed for Example 6

---

## 💡 Best Practices

### Prompt Engineering Tips

1. **Be Specific**
   - ❌ "Explain Python"
   - ✅ "Explain Python list comprehensions with 3 examples"

2. **Use Examples**
   - Few-shot > Zero-shot for format control

3. **Break Down Complex Tasks**
   - Use chain-of-thought for multi-step problems

4. **Iterate and Refine**
   - Test prompts
   - Analyze failures
   - Improve instructions

5. **Consider Token Costs**
   - Longer prompts = higher costs
   - Balance detail vs efficiency

### Security Best Practices

1. **Never hardcode API keys**
   - Always use environment variables
   - Use `.env` files
   - Add `.env` to `.gitignore`

2. **Validate User Input**
   - Sanitize inputs in production
   - Set rate limits
   - Monitor usage

3. **Handle Errors Gracefully**
   - Try-except blocks
   - User-friendly error messages
   - Logging for debugging

---

## 📚 Additional Resources

### Official Documentation
- [OpenAI API Docs](https://platform.openai.com/docs)
- [Google Gemini Docs](https://ai.google.dev/docs)
- [Prompt Engineering Guide](https://www.promptingguide.ai/)

### Learning Resources
- [OpenAI Cookbook](https://github.com/openai/openai-cookbook)
- [Awesome Prompt Engineering](https://github.com/promptslab/Awesome-Prompt-Engineering)

### Community
- [OpenAI Community Forum](https://community.openai.com/)
- [r/PromptEngineering](https://www.reddit.com/r/PromptEngineering/)

---

## 📝 License

This educational material is provided as-is for teaching purposes.

---

## 🤝 Contributing

Found an issue or want to improve the examples? Feel free to:
1. Report bugs
2. Suggest improvements
3. Add new examples
4. Improve documentation

---

## ❓ FAQ

**Q: Which model should I use?**
A: Start with `gpt-4o-mini` (cheap, fast). Upgrade to `gpt-4o` for complex tasks.

**Q: How much will this cost?**
A: Very little! These examples use minimal tokens. Expect < $0.10 for all examples.

**Q: Can I use this for production?**
A: These are educational examples. For production, add error handling, validation, and monitoring.

**Q: Do I need both OpenAI and Gemini keys?**
A: No! OpenAI key is enough for examples 1-5. Gemini is optional for example 6.

**Q: What if I get rate limited?**
A: Wait 60 seconds or upgrade your API tier.

---

**Happy Learning! 🚀**

For questions or issues, refer to the troubleshooting section or check the official documentation.
