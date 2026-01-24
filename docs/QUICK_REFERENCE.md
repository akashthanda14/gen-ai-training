# Quick Reference Guide - Prompt Engineering

## 🎯 When to Use Each Technique

| Technique | Use When | Example |
|-----------|----------|---------|
| **Zero-Shot** | Task is simple and clear | "Translate this to French" |
| **Few-Shot** | Need specific format | Return JSON with exact fields |
| **Chain-of-Thought** | Complex reasoning needed | Math problems, logic puzzles |
| **Persona-Based** | Need consistent character | Chatbots, brand voice |

---

## 📊 Comparison Table

| Aspect | Zero-Shot | Few-Shot | Chain-of-Thought | Persona |
|--------|-----------|----------|------------------|---------|
| **Complexity** | Low | Medium | High | Medium |
| **Token Usage** | Low | Medium | High | Medium |
| **Accuracy** | Medium | High | Very High | N/A |
| **Format Control** | Low | High | Medium | Low |
| **Setup Time** | Fast | Medium | Slow | Medium |

---

## 💰 Cost Optimization Tips

1. **Use cheaper models first**
   - `gpt-4o-mini` for testing
   - `gpt-4o` only when needed

2. **Minimize tokens**
   - Be concise but clear
   - Remove unnecessary examples
   - Cache system prompts when possible

3. **Batch requests**
   - Process multiple items together
   - Use async for parallel requests

---

## 🔑 Prompt Engineering Checklist

### Before Writing a Prompt:
- [ ] What is the exact task?
- [ ] What output format do I need?
- [ ] How complex is the reasoning?
- [ ] Do I have examples to show?

### Writing the Prompt:
- [ ] Clear instructions
- [ ] Specific output format
- [ ] Relevant examples (if few-shot)
- [ ] Edge case handling

### After Testing:
- [ ] Does it work consistently?
- [ ] Is the output format correct?
- [ ] Can I make it shorter?
- [ ] Are there edge cases to handle?

---

## 🎨 Prompt Templates

### Template 1: Classification
```python
SYSTEM_PROMPT = """
Classify the input into one of these categories: {categories}

Rules:
- Return only the category name
- If unsure, return "unknown"

Examples:
Input: {example_1_input}
Output: {example_1_output}

Input: {example_2_input}
Output: {example_2_output}
"""
```

### Template 2: JSON Output
```python
SYSTEM_PROMPT = """
Analyze the input and return JSON in this exact format:
{
    "field1": "type",
    "field2": "type",
    "field3": "type"
}

Examples:
Input: {example_input}
Output: {example_json}
"""
```

### Template 3: Step-by-Step
```python
SYSTEM_PROMPT = """
Solve the problem step by step:

1. Understand the problem
2. Break it into steps
3. Solve each step
4. Provide final answer

Show your work for each step.
"""
```

---

## 🚨 Common Mistakes to Avoid

### ❌ Mistake 1: Vague Instructions
```python
# Bad
"Tell me about Python"

# Good
"Explain Python list comprehensions with 3 examples showing filtering, mapping, and nested loops"
```

### ❌ Mistake 2: No Output Format
```python
# Bad
"Analyze this code"

# Good
"Analyze this code and return JSON: {\"issues\": [], \"score\": 0-10, \"suggestions\": []}"
```

### ❌ Mistake 3: Too Many Examples
```python
# Bad: 20 examples (wastes tokens)

# Good: 2-3 well-chosen examples
```

### ❌ Mistake 4: Hardcoded API Keys
```python
# Bad
client = OpenAI(api_key="sk-...")

# Good
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
```

---

## 📈 Progressive Learning Path

### Week 1: Basics
- [ ] Run all 6 examples
- [ ] Modify prompts
- [ ] Understand API structure

### Week 2: Practice
- [ ] Build a classifier (few-shot)
- [ ] Create a chatbot (persona)
- [ ] Solve math problems (CoT)

### Week 3: Advanced
- [ ] Combine techniques
- [ ] Optimize for cost
- [ ] Handle edge cases

### Week 4: Production
- [ ] Error handling
- [ ] Rate limiting
- [ ] Monitoring and logging

---

## 🎓 Exercise Solutions

### Exercise 1: Code Reviewer
```python
SYSTEM_PROMPT = """
Review code and return JSON:
{
    "issues": ["list of problems"],
    "score": 0-10,
    "suggestions": ["list of improvements"]
}

Example:
Code: def add(a,b): return a+b
Output: {
    "issues": ["No type hints", "No docstring"],
    "score": 6,
    "suggestions": ["Add type hints", "Add docstring", "Add input validation"]
}
"""
```

### Exercise 2: Math Tutor
```python
SYSTEM_PROMPT = """
Solve word problems step by step:

1. Identify what we know
2. Identify what we need to find
3. Choose the operation
4. Calculate
5. Check if answer makes sense

Show all steps clearly.
"""
```

---

## 🔗 Quick Links

- [OpenAI Pricing](https://openai.com/pricing)
- [Gemini Pricing](https://ai.google.dev/pricing)
- [Prompt Engineering Guide](https://www.promptingguide.ai/)
- [OpenAI Best Practices](https://platform.openai.com/docs/guides/prompt-engineering)

---

## 💡 Pro Tips

1. **Test with edge cases**
   - Empty input
   - Very long input
   - Unexpected formats

2. **Version your prompts**
   - Track what works
   - A/B test changes
   - Document improvements

3. **Monitor performance**
   - Response time
   - Token usage
   - Error rates

4. **Iterate quickly**
   - Start simple
   - Add complexity gradually
   - Measure improvements

---

**Keep this guide handy while learning! 📚**
