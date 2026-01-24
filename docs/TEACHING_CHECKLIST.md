# Teaching Checklist - Prompt Engineering Course

## 📋 Pre-Class Preparation

### For Instructor:
- [ ] Verify all example files run successfully
- [ ] Test API keys are working
- [ ] Prepare backup API keys (in case of rate limits)
- [ ] Review README.md thoroughly
- [ ] Prepare real-world use case examples
- [ ] Set up screen sharing/projection
- [ ] Have QUICK_REFERENCE.md open for reference

### For Students:
- [ ] Python 3.8+ installed
- [ ] Text editor/IDE installed (VS Code, PyCharm, etc.)
- [ ] OpenAI account created
- [ ] API key obtained and tested
- [ ] Repository downloaded/cloned
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] `.env` file configured with API key

---

## 🎓 Session 1: Foundations (30-45 min)

### Introduction (10 min)
- [ ] What are LLMs? (ChatGPT, GPT-4, Gemini, etc.)
- [ ] API vs Web Interface
- [ ] Why prompt engineering matters
- [ ] Real-world applications

### Demo: Hello World (10 min)
- [ ] Open `01_hello_world.py`
- [ ] Explain code structure line by line
- [ ] Explain system vs user roles
- [ ] Run the example live
- [ ] Show response in terminal

### Hands-On Exercise 1 (15 min)
**Task:** Modify the hello world example
- [ ] Change the system prompt (make it a history expert)
- [ ] Change the user question
- [ ] Run and observe results
- [ ] Discuss: How does system prompt affect responses?

### Wrap-Up (5 min)
- [ ] Q&A
- [ ] Preview next session
- [ ] Assign homework: Experiment with different system prompts

---

## 🎓 Session 2: Zero-Shot vs Few-Shot (45-60 min)

### Zero-Shot Prompting (15 min)
- [ ] Open `02_zero_shot_prompting.py`
- [ ] Explain the concept: instructions without examples
- [ ] Run the example
- [ ] Show when it works well
- [ ] Show limitations (inconsistent format)

### Few-Shot Prompting (15 min)
- [ ] Open `03_few_shot_prompting.py`
- [ ] Explain the concept: learning from examples
- [ ] Run the example
- [ ] Compare output with zero-shot
- [ ] Highlight format consistency

### Comparison Discussion (10 min)
- [ ] When to use zero-shot?
  - Simple tasks
  - Quick queries
  - No specific format needed
- [ ] When to use few-shot?
  - Need consistent format
  - Complex output structure
  - JSON/structured data

### Hands-On Exercise 2 (20 min)
**Task:** Build a sentiment analyzer

**Zero-Shot Version:**
```python
SYSTEM_PROMPT = "Classify the sentiment as positive, negative, or neutral"
```

**Few-Shot Version:**
```python
SYSTEM_PROMPT = """
Classify sentiment and return JSON: {"sentiment": "positive|negative|neutral", "confidence": 0-1}

Examples:
"I love this!" → {"sentiment": "positive", "confidence": 0.95}
"This is terrible" → {"sentiment": "negative", "confidence": 0.9}
"It's okay" → {"sentiment": "neutral", "confidence": 0.7}
"""
```

- [ ] Students implement both versions
- [ ] Test with different inputs
- [ ] Compare results
- [ ] Discuss which is better and why

---

## 🎓 Session 3: Advanced Techniques (60 min)

### Chain-of-Thought (20 min)
- [ ] Open `04_chain_of_thought.py`
- [ ] Explain the concept: step-by-step reasoning
- [ ] Show example: Solve a math problem
  - Without CoT: Direct answer (might be wrong)
  - With CoT: Shows reasoning steps (more accurate)
- [ ] Run the example
- [ ] Discuss when CoT is essential

### Hands-On Exercise 3 (15 min)
**Task:** Math word problem solver

Problem: "Sarah has 15 apples. She gives 1/3 to John and 20% of the remainder to Mary. How many does she have left?"

- [ ] Students implement CoT prompt
- [ ] Verify step-by-step reasoning
- [ ] Check final answer
- [ ] Discuss: Would zero-shot work here?

### Persona-Based Prompting (15 min)
- [ ] Open `05_persona_based_prompting.py`
- [ ] Explain the concept: AI with personality
- [ ] Show the Karanvir persona example
- [ ] Run interactive demo
- [ ] Discuss use cases:
  - Customer support bots
  - Educational tutors
  - Brand voice consistency

### Hands-On Exercise 4 (10 min)
**Task:** Create a custom persona

Examples:
- Friendly tech support agent
- Pirate storyteller
- Professional business consultant
- Enthusiastic fitness coach

- [ ] Students pick a persona
- [ ] Write system prompt with examples
- [ ] Test with various questions
- [ ] Share results with class

---

## 🎓 Session 4: Different Providers & Best Practices (45 min)

### Google Gemini Example (10 min)
- [ ] Open `06_gemini_example.py`
- [ ] Compare API structure with OpenAI
- [ ] Discuss pros/cons of different providers
- [ ] Run example (if students have Gemini key)

### Best Practices (15 min)
- [ ] **Security:**
  - Never hardcode API keys
  - Use environment variables
  - Add `.env` to `.gitignore`
  
- [ ] **Cost Optimization:**
  - Use cheaper models for testing
  - Minimize token usage
  - Cache when possible
  
- [ ] **Prompt Engineering:**
  - Be specific
  - Iterate and refine
  - Test edge cases
  - Version your prompts

### Real-World Project Discussion (10 min)
Show examples of production use cases:
- [ ] Customer support chatbot
- [ ] Code review assistant
- [ ] Content generation tool
- [ ] Data extraction from documents

### Final Exercise (10 min)
**Task:** Combine techniques

Build a "Smart Code Reviewer" that:
1. Uses few-shot for JSON output format
2. Uses CoT to explain issues
3. Uses persona (professional but friendly)

```python
SYSTEM_PROMPT = """
You are a friendly senior developer reviewing code.

Use this format:
{
    "issues": [...],
    "score": 0-10,
    "explanation": "step-by-step reasoning",
    "suggestions": [...]
}

Example:
Code: def add(a,b): return a+b

Reasoning:
1. Function works but lacks documentation
2. No type hints for clarity
3. No input validation
4. Score: 6/10 (functional but not production-ready)

Output: {
    "issues": ["No docstring", "No type hints", "No validation"],
    "score": 6,
    "explanation": "...",
    "suggestions": ["Add docstring", "Add type hints", "Validate inputs"]
}
"""
```

---

## 📝 Assessment & Evaluation

### Knowledge Check Questions:

1. **What's the difference between zero-shot and few-shot?**
   - Expected: Zero-shot = no examples, few-shot = with examples

2. **When should you use chain-of-thought?**
   - Expected: Complex reasoning, math problems, multi-step tasks

3. **Why use environment variables for API keys?**
   - Expected: Security, avoid hardcoding secrets

4. **How do you make output format consistent?**
   - Expected: Use few-shot prompting with format examples

5. **What's the trade-off of longer prompts?**
   - Expected: More control but higher token cost

### Practical Assessment:

**Final Project:** Build a practical application using learned techniques

Options:
1. **Email Classifier**
   - Classify emails (spam/important/newsletter)
   - Extract key information
   - Suggest actions

2. **Study Buddy**
   - Answer questions with explanations
   - Use CoT for problem-solving
   - Friendly tutor persona

3. **Code Helper**
   - Review code quality
   - Suggest improvements
   - Explain concepts

Requirements:
- [ ] Use at least 2 different techniques
- [ ] Proper error handling
- [ ] Environment variables for API key
- [ ] Clear documentation
- [ ] Test with multiple inputs

---

## 🎯 Learning Outcomes

By the end of this course, students should be able to:

- [ ] Understand how LLM APIs work
- [ ] Write effective prompts for different tasks
- [ ] Choose the right prompting technique
- [ ] Implement zero-shot prompting
- [ ] Implement few-shot prompting with examples
- [ ] Use chain-of-thought for complex reasoning
- [ ] Create persona-based prompts
- [ ] Handle API keys securely
- [ ] Optimize for cost and performance
- [ ] Debug and iterate on prompts
- [ ] Build real-world applications

---

## 📚 Additional Resources to Share

### Documentation:
- OpenAI API Docs: https://platform.openai.com/docs
- Prompt Engineering Guide: https://www.promptingguide.ai/
- OpenAI Cookbook: https://github.com/openai/openai-cookbook

### Practice:
- PromptBase (prompt marketplace): https://promptbase.com/
- Learn Prompting: https://learnprompting.org/
- Awesome Prompts: https://github.com/f/awesome-chatgpt-prompts

### Community:
- OpenAI Community: https://community.openai.com/
- r/PromptEngineering: https://reddit.com/r/PromptEngineering

---

## ✅ Post-Class Follow-Up

### For Instructor:
- [ ] Share recording (if applicable)
- [ ] Share additional resources
- [ ] Provide feedback on exercises
- [ ] Answer follow-up questions
- [ ] Share advanced topics for further learning

### For Students:
- [ ] Complete final project
- [ ] Experiment with different models
- [ ] Join community forums
- [ ] Build portfolio projects
- [ ] Share learnings with peers

---

## 🎓 Certificate Criteria (Optional)

Students earn completion certificate by:
- [ ] Attending all sessions (or watching recordings)
- [ ] Completing all hands-on exercises
- [ ] Submitting final project
- [ ] Demonstrating understanding in Q&A
- [ ] Passing knowledge check (80%+)

---

## 💡 Tips for Effective Teaching

1. **Start Simple**
   - Don't overwhelm with theory
   - Show working examples first
   - Build complexity gradually

2. **Hands-On Focus**
   - More coding, less slides
   - Let students experiment
   - Encourage breaking things

3. **Real-World Context**
   - Show actual use cases
   - Discuss industry applications
   - Share success stories

4. **Encourage Questions**
   - No question is too basic
   - Create safe learning environment
   - Use questions to teach

5. **Iterate and Adapt**
   - Adjust pace based on class
   - Skip ahead if too easy
   - Slow down if struggling

---

**Good luck with your teaching! 🚀**

Remember: The goal is not just to teach syntax, but to help students think like prompt engineers!
