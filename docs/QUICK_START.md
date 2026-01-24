# 🚀 Quick Start Guide

**New to prompt engineering? Start here!**

This is a 5-minute guide to get you up and running.

---

## ⚡ Super Quick Setup (5 minutes)

### Step 1: Get an API Key (2 minutes)
1. Go to [OpenAI Platform](https://platform.openai.com/signup)
2. Sign up for an account
3. Go to [API Keys](https://platform.openai.com/api-keys)
4. Click "Create new secret key"
5. Copy the key (starts with `sk-...`)

### Step 2: Install Python Packages (1 minute)
```bash
pip install openai python-dotenv
```

### Step 3: Configure Your API Key (1 minute)
Create a file named `.env` in this folder:
```bash
OPENAI_API_KEY=sk-your-actual-key-here
```

### Step 4: Test It Works (1 minute)
```bash
python verify_setup.py
```

If you see "All checks passed! 🎉" - you're ready!

---

## 🎯 Your First Prompt (2 minutes)

Run this:
```bash
python 01_hello_world.py
```

You should see the AI respond to a math question!

---

## 📚 What to Learn Next

Follow this order:

1. **Day 1:** Run `01_hello_world.py` and understand the code
2. **Day 2:** Try `02_zero_shot_prompting.py` - direct instructions
3. **Day 3:** Try `03_few_shot_prompting.py` - learning from examples
4. **Day 4:** Try `04_chain_of_thought.py` - step-by-step reasoning
5. **Day 5:** Try `05_persona_based_prompting.py` - AI with personality

---

## 🆘 Something Not Working?

### Problem: "OPENAI_API_KEY is not set"
**Solution:** Make sure you created the `.env` file with your API key

### Problem: "No module named 'openai'"
**Solution:** Run `pip install -r requirements.txt`

### Problem: "Invalid API key"
**Solution:** 
1. Check your key starts with `sk-`
2. Make sure you copied the entire key
3. Try generating a new key from OpenAI

### Still stuck?
Check the **Troubleshooting** section in `README.md`

---

## 📖 Full Documentation

- **README.md** - Complete guide with all details
- **QUICK_REFERENCE.md** - Tips and templates
- **TEACHING_CHECKLIST.md** - For instructors

---

## 💡 Quick Tips

1. **Start simple** - Don't try to understand everything at once
2. **Experiment** - Change the prompts and see what happens
3. **Read the comments** - Each file has detailed explanations
4. **Ask questions** - There are no stupid questions!

---

## 🎓 Learning Path

```
Week 1: Basics
├── Understand what LLMs are
├── Run all 6 examples
└── Modify prompts and experiment

Week 2: Practice
├── Build a simple classifier
├── Create a chatbot
└── Solve problems with CoT

Week 3: Projects
├── Combine techniques
├── Build something useful
└── Share with others
```

---

## ✅ Success Checklist

- [ ] API key configured
- [ ] All examples run successfully
- [ ] Understand zero-shot vs few-shot
- [ ] Can write effective prompts
- [ ] Built at least one project

---

**Ready? Start with `python 01_hello_world.py`** 🚀

For detailed explanations, open `README.md`
