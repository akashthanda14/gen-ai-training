"""
Module 1: Alpaca Prompt Format
===============================
The "Hidden" Language of LLMs - Part 1

Goal: Understand that LLMs don't just "understand" chat - they expect
specific raw string formats based on how they were trained.

Alpaca Format Origin: Stanford's Alpaca model (fine-tuned LLaMA 1)
Use Case: Older open-source models, simple instruction following
"""

import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


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
    # Start with the Instruction header
    # Note: Must be exactly "### Instruction:" with capital I and colon
    prompt = "### Instruction:\n"
    
    # Add the actual instruction text
    # \n\n creates a blank line after the instruction for readability
    prompt += f"{instruction}\n\n"
    
    # Only add Input section if input_data is provided
    # This is optional - simple tasks don't need it
    if input_data:
        # Input header - exactly "### Input:" with capital I
        prompt += "### Input:\n"
        
        # Add the input data (context, text to process, etc.)
        # Again, \n\n creates a blank line for separation
        prompt += f"{input_data}\n\n"
    
    # Always end with Response header
    # This tells the model "start generating your answer here"
    prompt += "### Response:\n"
    
    # Optional: Add a prefix to guide the response format
    # Example: "Sure, here is the translation:" or "{"
    if response_prefix:
        prompt += response_prefix
    
    # Return the complete formatted prompt
    # The model will see this exact string with all the \n newlines
    return prompt


# ============================================================================
# Example 1: Simple Instruction (No Input)
# ============================================================================
# This example shows the simplest form of Alpaca format:
# Just an instruction, no input data needed

print("=" * 70)
print("Example 1: Simple Instruction (No Input)")
print("=" * 70)

# Define a simple instruction - just tell the model what to do
instruction1 = "Write a haiku about artificial intelligence."

# Create the Alpaca-formatted prompt
# This function wraps our instruction in the proper format
alpaca_prompt1 = create_alpaca_prompt(instruction1)

# Show the RAW STRING - this is what the model ACTUALLY receives
print("\n📝 RAW STRING (What the model sees):")
print("-" * 70)
# repr() shows the string with visible \n characters
# This helps you see the exact format including newlines
print(repr(alpaca_prompt1))  
print("-" * 70)

# Show the FORMATTED view - how it looks when printed normally
print("\n📄 FORMATTED VIEW:")
print("-" * 70)
# Without repr(), \n becomes actual line breaks
print(alpaca_prompt1)
print("-" * 70)

# Send the formatted prompt to the model
# We're using OpenAI's API, but the Alpaca format works with any model
response1 = client.chat.completions.create(
    model="gpt-4o-mini",  # The model to use
    messages=[{"role": "user", "content": alpaca_prompt1}],  # Our Alpaca-formatted prompt
    temperature=0.7  # Controls randomness (0.7 = balanced creativity)
)

# Extract and print the model's response
print("\n🤖 MODEL RESPONSE:")
# The response is in response1.choices[0].message.content
print(response1.choices[0].message.content)
print()


# ============================================================================
# Example 2: Instruction WITH Input Context
# ============================================================================

print("=" * 70)
print("Example 2: Instruction WITH Input Context")
print("=" * 70)

instruction2 = "Summarize the following text in one sentence."
input_data2 = """
Artificial intelligence is rapidly transforming industries worldwide. 
From healthcare diagnostics to financial fraud detection, AI systems 
are becoming increasingly sophisticated. Machine learning algorithms 
can now process vast amounts of data and identify patterns that humans 
might miss.
"""

alpaca_prompt2 = create_alpaca_prompt(instruction2, input_data2)

print("\n📝 RAW STRING (What the model sees):")
print("-" * 70)
print(repr(alpaca_prompt2))
print("-" * 70)

print("\n📄 FORMATTED VIEW:")
print("-" * 70)
print(alpaca_prompt2)
print("-" * 70)

response2 = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": alpaca_prompt2}],
    temperature=0.3
)

print("\n🤖 MODEL RESPONSE:")
print(response2.choices[0].message.content)
print()


# ============================================================================
# Example 3: Data Extraction Task
# ============================================================================

print("=" * 70)
print("Example 3: Data Extraction Task")
print("=" * 70)

instruction3 = "Extract the person's name, age, and occupation from the text. Format as JSON."
input_data3 = "My name is Sarah Johnson, I'm 32 years old, and I work as a software engineer at Tech Corp."

alpaca_prompt3 = create_alpaca_prompt(instruction3, input_data3)

print("\n📝 RAW STRING:")
print("-" * 70)
print(repr(alpaca_prompt3))
print("-" * 70)

response3 = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": alpaca_prompt3}],
    temperature=0.1
)

print("\n🤖 MODEL RESPONSE:")
print(response3.choices[0].message.content)
print()


# ============================================================================
# Example 4: Few-Shot Learning with Alpaca
# ============================================================================

print("=" * 70)
print("Example 4: Few-Shot Learning")
print("=" * 70)

instruction4 = """Classify the sentiment of the given text as POSITIVE, NEGATIVE, or NEUTRAL.

Examples:
Text: "I love this product!" -> POSITIVE
Text: "This is terrible." -> NEGATIVE
Text: "It's okay." -> NEUTRAL

Now classify the following:"""

input_data4 = "The movie was absolutely fantastic! Best film I've seen this year."

alpaca_prompt4 = create_alpaca_prompt(instruction4, input_data4)

print("\n📄 FORMATTED VIEW:")
print("-" * 70)
print(alpaca_prompt4)
print("-" * 70)

response4 = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": alpaca_prompt4}],
    temperature=0.1
)

print("\n🤖 MODEL RESPONSE:")
print(response4.choices[0].message.content)
print()


# ============================================================================
# Example 5: Code Generation
# ============================================================================

print("=" * 70)
print("Example 5: Code Generation")
print("=" * 70)

instruction5 = "Write a Python function to calculate the factorial of a number using recursion. Include docstring and type hints."

alpaca_prompt5 = create_alpaca_prompt(instruction5)

print("\n📄 FORMATTED VIEW:")
print("-" * 70)
print(alpaca_prompt5)
print("-" * 70)

response5 = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": alpaca_prompt5}],
    temperature=0.2
)

print("\n🤖 MODEL RESPONSE:")
print(response5.choices[0].message.content)
print()


# ============================================================================
# Teaching Points
# ============================================================================

print("=" * 70)
print("🎓 KEY TEACHING POINTS")
print("=" * 70)

print("""
1. THE RAW STRING MATTERS
   -------------------------
   When you see:
   
   ### Instruction:
   Write a haiku
   
   ### Response:
   
   This is the ACTUAL string the model receives. Not a chat interface,
   not a JSON object - just this exact text with these exact newlines.

2. STRUCTURE IS EXPLICIT
   ----------------------
   The model was trained to recognize:
   - "### Instruction:" as the start of a task
   - "### Input:" as optional context
   - "### Response:" as where it should start answering
   
   If you change these headers, the model gets confused!

3. WHY ALPACA FORMAT EXISTS
   -------------------------
   Stanford created this format to fine-tune LLaMA 1 on instructions.
   They needed a consistent way to show the model:
   - What to do (Instruction)
   - What data to use (Input)
   - Where to respond (Response)

4. WHEN TO USE ALPACA
   -------------------
   ✅ Older open-source models (Alpaca, Vicuna)
   ✅ Simple instruction-following tasks
   ✅ Single-turn interactions
   ❌ Modern chat models (use ChatML instead)
   ❌ Multi-turn conversations

5. COMMON MISTAKES
   ----------------
   ❌ Forgetting the "###" markers
   ❌ Wrong capitalization (it's "Instruction" not "instruction")
   ❌ Missing newlines between sections
   ❌ Using with models trained on different formats

6. COMPARISON TO NORMAL PROMPTING
   -------------------------------
   Normal: "Summarize this text: [text]"
   Alpaca: 
   ### Instruction:
   Summarize the following text in one sentence.
   
   ### Input:
   [text]
   
   ### Response:
   
   The Alpaca format is MORE EXPLICIT about what's instruction vs. data.
""")


# ============================================================================
# Interactive Demo
# ============================================================================

print("\n" + "=" * 70)
print("🔬 INTERACTIVE DEMO: See the Difference")
print("=" * 70)

demo_task = "Translate 'Hello, how are you?' to French."

print("\n1️⃣  WITHOUT Alpaca Format (Plain Prompt):")
print("-" * 70)
plain_prompt = demo_task
print(f"Prompt: {plain_prompt}")

response_plain = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": plain_prompt}],
    temperature=0.3
)

print(f"Response: {response_plain.choices[0].message.content}")

print("\n2️⃣  WITH Alpaca Format:")
print("-" * 70)
alpaca_demo = create_alpaca_prompt(demo_task)
print(f"Prompt:\n{alpaca_demo}")

response_alpaca = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": alpaca_demo}],
    temperature=0.3
)

print(f"Response: {response_alpaca.choices[0].message.content}")

print("\n💡 OBSERVATION:")
print("Both work with GPT-4, but Alpaca format provides more structure.")
print("With older models, the Alpaca format would work MUCH better!")


print("\n" + "=" * 70)
print("✅ Module 1 - Alpaca Format Complete!")
print("=" * 70)
print("\nNext: Run chatml_format.py to learn ChatML (OpenAI's format)")
