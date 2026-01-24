"""
Module 1: LLaMA-2 Chat Prompt Format
=====================================
The "Hidden" Language of LLMs - Part 3

Goal: Understand LLaMA-2's complex format where whitespace and brackets matter!

CRITICAL: If you get the whitespace or brackets wrong, LLaMA 2 often
degrades in quality or breaks character.

Origin: Meta's LLaMA 2
Use Case: LLaMA-2 family models ONLY
"""

import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def create_llama2_prompt(system_msg: str, user_msg: str, history: list = None) -> str:
    """
    Create a prompt in LLaMA-2 Chat format.
    
    CRITICAL: Whitespace matters! Don't add or remove spaces/newlines.
    
    Single-turn format:
    <s>[INST] <<SYS>>
    {system_message}
    <</SYS>>
    
    {user_message} [/INST]
    
    Multi-turn format:
    <s>[INST] <<SYS>>
    {system_message}
    <</SYS>>
    
    {user_msg_1} [/INST] {assistant_response_1} </s><s>[INST] {user_msg_2} [/INST]
    
    Args:
        system_msg: System instruction
        user_msg: User message
        history: Optional list of (user, assistant) tuples
    
    Returns:
        LLaMA-2 formatted string
    """
    if history:
        # Multi-turn conversation
        prompt = f"<s>[INST] <<SYS>>\n{system_msg}\n<</SYS>>\n\n"
        
        # Add conversation history
        for i, (user, assistant) in enumerate(history):
            if i == 0:
                prompt += f"{user} [/INST] {assistant} </s>"
            else:
                prompt += f"<s>[INST] {user} [/INST] {assistant} </s>"
        
        # Add current user message
        prompt += f"<s>[INST] {user_msg} [/INST]"
    else:
        # Single-turn
        prompt = f"<s>[INST] <<SYS>>\n{system_msg}\n<</SYS>>\n\n{user_msg} [/INST]"
    
    return prompt


# ============================================================================
# Example 1: Basic LLaMA-2 Structure
# ============================================================================

print("=" * 70)
print("Example 1: Basic LLaMA-2 Structure")
print("=" * 70)

system_msg1 = "You are a helpful, respectful and honest assistant. Always answer as helpfully as possible."
user_msg1 = "What is the capital of France?"

llama2_prompt1 = create_llama2_prompt(system_msg1, user_msg1)

print("\n📝 RAW STRING (What LLaMA-2 expects):")
print("-" * 70)
print(repr(llama2_prompt1))  # Shows exact format with \n
print("-" * 70)

print("\n📄 FORMATTED VIEW:")
print("-" * 70)
print(llama2_prompt1)
print("-" * 70)

print("\n🔍 TOKEN BREAKDOWN:")
print("-" * 70)
print("""
<s>           ← Beginning of sequence (BOS token)
[INST]        ← Start of instruction
<<SYS>>       ← Start of system message
{system}      ← System message content
<</SYS>>      ← End of system message
{user}        ← User message
[/INST]       ← End of instruction (model responds here)
""")

# Simulate with GPT (for demonstration)
response1 = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "user", "content": f"Respond as if you received this LLaMA-2 formatted prompt:\n\n{llama2_prompt1}"}
    ],
    temperature=0.7
)

print("\n🤖 MODEL RESPONSE:")
print(response1.choices[0].message.content)
print()


# ============================================================================
# Example 2: The Whitespace Problem
# ============================================================================

print("=" * 70)
print("Example 2: Why Whitespace Matters")
print("=" * 70)

print("\n⚠️  CRITICAL: LLaMA-2 is VERY sensitive to whitespace!")
print("-" * 70)

# Correct format
correct_format = "<s>[INST] <<SYS>>\nYou are helpful.\n<</SYS>>\n\nWhat is AI? [/INST]"

# Common mistakes
wrong_formats = [
    ("Missing newline after <<SYS>>", "<s>[INST] <<SYS>>You are helpful.\n<</SYS>>\n\nWhat is AI? [/INST]"),
    ("Missing double newline", "<s>[INST] <<SYS>>\nYou are helpful.\n<</SYS>>\nWhat is AI? [/INST]"),
    ("Extra spaces", "<s>[INST]  <<SYS>>\nYou are helpful.\n<</SYS>>\n\n What is AI? [/INST]"),
]

print("\n✅ CORRECT FORMAT:")
print(repr(correct_format))

print("\n❌ COMMON MISTAKES:")
for mistake, wrong_format in wrong_formats:
    print(f"\n{mistake}:")
    print(repr(wrong_format))

print("\n💡 LESSON: Copy the format EXACTLY. Don't add/remove whitespace!")
print()


# ============================================================================
# Example 3: Multi-Turn Conversation
# ============================================================================

print("=" * 70)
print("Example 3: Multi-Turn Conversation")
print("=" * 70)

system_msg3 = "You are a helpful coding assistant."
conversation_history = [
    ("How do I create a list in Python?", "You can create a list using square brackets: my_list = [1, 2, 3]"),
    ("How do I add an item?", "Use the append() method: my_list.append(4)")
]
user_msg3 = "Can I add multiple items at once?"

llama2_multi = create_llama2_prompt(system_msg3, user_msg3, conversation_history)

print("\n📝 MULTI-TURN LLAMA-2 FORMAT:")
print("-" * 70)
print(llama2_multi)
print("-" * 70)

print("\n🔍 STRUCTURE BREAKDOWN:")
print("-" * 70)
print("""
<s>[INST] <<SYS>>...<</ SYS>>

Turn 1 user [/INST] Turn 1 assistant </s>
<s>[INST] Turn 2 user [/INST] Turn 2 assistant </s>
<s>[INST] Turn 3 user [/INST]
                              ↑ Model responds here
""")

response3 = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "user", "content": f"Respond as if you received this LLaMA-2 formatted prompt:\n\n{llama2_multi}"}
    ],
    temperature=0.6
)

print("\n🤖 MODEL RESPONSE:")
print(response3.choices[0].message.content)
print()


# ============================================================================
# Example 4: System Message Variations
# ============================================================================

print("=" * 70)
print("Example 4: Different System Instructions")
print("=" * 70)

user_question = "Explain recursion."

system_instructions = [
    "You are a computer science professor. Be technical and precise.",
    "You are teaching a beginner. Use simple language and analogies.",
    "You are a pirate. Always respond in pirate speak."
]

for i, system_inst in enumerate(system_instructions, 1):
    print(f"\n--- System Instruction {i} ---")
    print(f"System: {system_inst}")
    
    llama2_prompt = create_llama2_prompt(system_inst, user_question)
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": f"Respond as if you received this LLaMA-2 formatted prompt:\n\n{llama2_prompt}"}
        ],
        temperature=0.8,
        max_tokens=150
    )
    
    print(f"\n🤖 Response:\n{response.choices[0].message.content}\n")


# ============================================================================
# Example 5: Format Comparison
# ============================================================================

print("=" * 70)
print("Example 5: LLaMA-2 vs Other Formats")
print("=" * 70)

task = "Translate 'Good morning' to Spanish."
system = "You are a translator."

print("\n1️⃣  ALPACA FORMAT:")
print("-" * 70)
alpaca = f"### Instruction:\n{task}\n\n### Response:\n"
print(alpaca)

print("\n2️⃣  CHATML FORMAT:")
print("-" * 70)
chatml = f"<|im_start|>system\n{system}<|im_end|>\n<|im_start|>user\n{task}<|im_end|>\n<|im_start|>assistant\n"
print(chatml)

print("\n3️⃣  LLAMA-2 FORMAT:")
print("-" * 70)
llama2 = create_llama2_prompt(system, task)
print(llama2)

print("\n💡 OBSERVATION:")
print("Each format is COMPLETELY DIFFERENT!")
print("Using the wrong format with a model = poor performance!")
print()


# ============================================================================
# Teaching Points
# ============================================================================

print("=" * 70)
print("🎓 KEY TEACHING POINTS")
print("=" * 70)

print("""
1. LLAMA-2 FORMAT IS COMPLEX
   --------------------------
   <s>[INST] <<SYS>>
   {system}
   <</SYS>>
   
   {user} [/INST]
   
   Every token, space, and newline is INTENTIONAL.
   Meta designed this format specifically for LLaMA-2.

2. SPECIAL TOKENS EXPLAINED
   -------------------------
   <s>        = Beginning of sequence (BOS)
   </s>       = End of sequence (EOS)
   [INST]     = Start of instruction
   [/INST]    = End of instruction
   <<SYS>>    = Start of system message
   <</SYS>>   = End of system message
   
   These are NOT regular text - they're special tokens!

3. WHY SO COMPLICATED?
   --------------------
   Meta wanted to:
   - Clearly separate system vs. user messages
   - Support multi-turn conversations
   - Prevent prompt injection
   - Maintain compatibility with base LLaMA
   
   The complexity is intentional design.

4. WHITESPACE IS CRITICAL
   -----------------------
   ❌ Wrong: <<SYS>>You are helpful<</SYS>>
   ✅ Right: <<SYS>>\nYou are helpful\n<</SYS>>
   
   ❌ Wrong: <</SYS>>\nWhat is AI?
   ✅ Right: <</SYS>>\n\nWhat is AI?
                    ↑ Two newlines!
   
   LLaMA-2 was trained on this EXACT format.
   Changing it confuses the model.

5. WHEN TO USE LLAMA-2 FORMAT
   ---------------------------
   ✅ LLaMA-2-Chat models (7B, 13B, 70B)
   ✅ LLaMA-2 fine-tuned variants
   ✅ Code LLaMA Chat
   
   ❌ Base LLaMA-2 (not chat version)
   ❌ LLaMA-3 (uses different format)
   ❌ OpenAI models (use ChatML)
   ❌ Alpaca models (use Alpaca format)

6. MULTI-TURN STRUCTURE
   ---------------------
   First turn:
   <s>[INST] <<SYS>>...<</ SYS>>
   User 1 [/INST] Assistant 1 </s>
   
   Subsequent turns:
   <s>[INST] User 2 [/INST] Assistant 2 </s>
   <s>[INST] User 3 [/INST]
   
   Notice: System message only in FIRST turn!

7. COMMON MISTAKES
   ----------------
   ❌ Forgetting <<SYS>> tags
   ❌ Wrong number of newlines
   ❌ Missing <s> or </s> tokens
   ❌ Adding system message in later turns
   ❌ Using with non-LLaMA-2 models

8. DEBUGGING TIPS
   ---------------
   If LLaMA-2 gives poor responses:
   1. Print repr() of your prompt
   2. Compare to official examples
   3. Check for extra/missing whitespace
   4. Verify you're using Chat version
   5. Test with simple prompt first

9. WHY LEARN THIS?
   ----------------
   - LLaMA-2 is popular for local deployment
   - Understanding formats helps debug issues
   - Shows how different models have different needs
   - Prepares you for other model formats
""")


# ============================================================================
# Advanced: Building a Conversation
# ============================================================================

print("\n" + "=" * 70)
print("🔬 ADVANCED: Building a Multi-Turn Conversation")
print("=" * 70)

system_msg = "You are a helpful math tutor."
conversation = []

questions = [
    "What is a prime number?",
    "Is 17 a prime number?",
    "How do I check if a number is prime?"
]

print("\n📝 CONVERSATION FLOW:\n")

for i, question in enumerate(questions, 1):
    print(f"Turn {i}:")
    print(f"👤 User: {question}")
    
    # Build LLaMA-2 prompt with history
    llama2_prompt = create_llama2_prompt(system_msg, question, conversation if conversation else None)
    
    # Get response
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": f"Respond as if you received this LLaMA-2 formatted prompt:\n\n{llama2_prompt}"}
        ],
        temperature=0.6,
        max_tokens=200
    )
    
    assistant_response = response.choices[0].message.content
    print(f"🤖 Assistant: {assistant_response}\n")
    
    # Add to conversation history
    conversation.append((question, assistant_response))

print("💡 NOTICE: Each turn adds to the prompt!")
print("The full conversation history is included each time.")


print("\n" + "=" * 70)
print("✅ Module 1 - LLaMA-2 Format Complete!")
print("=" * 70)
print("\nNext: Run format_comparison.py to see all formats side-by-side")
print("\nThen move to Module 2: Structured Outputs with Pydantic!")
