"""
11. OpenAI Advanced Features
=============================
Demonstrates advanced OpenAI API features including streaming,
function calling, vision capabilities, and JSON mode.

Key Concepts:
- Streaming responses for real-time output
- Function calling for tool integration
- Vision API (GPT-4V) for image analysis
- JSON mode for structured outputs
- Token management and optimization
"""

import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


# Example 1: Streaming Responses
print("=" * 60)
print("Example 1: Streaming Responses")
print("=" * 60)

print("\n🔄 Streaming response (real-time):\n")

stream = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "user", "content": "Write a short poem about artificial intelligence."}
    ],
    stream=True,  # Enable streaming
    temperature=0.8
)

# Print tokens as they arrive
for chunk in stream:
    if chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end="", flush=True)

print("\n")


# Example 2: Function Calling
print("=" * 60)
print("Example 2: Function Calling (Tools)")
print("=" * 60)

# Define functions that the model can call
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get the current weather for a location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "City name, e.g. San Francisco"
                    },
                    "unit": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"],
                        "description": "Temperature unit"
                    }
                },
                "required": ["location"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate_mortgage",
            "description": "Calculate monthly mortgage payment",
            "parameters": {
                "type": "object",
                "properties": {
                    "principal": {
                        "type": "number",
                        "description": "Loan amount in dollars"
                    },
                    "interest_rate": {
                        "type": "number",
                        "description": "Annual interest rate (e.g., 3.5 for 3.5%)"
                    },
                    "years": {
                        "type": "integer",
                        "description": "Loan term in years"
                    }
                },
                "required": ["principal", "interest_rate", "years"]
            }
        }
    }
]

# Simulate function implementations
def get_weather(location: str, unit: str = "celsius") -> dict:
    """Simulated weather API call."""
    # In real scenario, this would call an actual weather API
    return {
        "location": location,
        "temperature": 22 if unit == "celsius" else 72,
        "unit": unit,
        "condition": "Sunny"
    }

def calculate_mortgage(principal: float, interest_rate: float, years: int) -> dict:
    """Calculate monthly mortgage payment."""
    monthly_rate = interest_rate / 100 / 12
    num_payments = years * 12
    
    if monthly_rate == 0:
        monthly_payment = principal / num_payments
    else:
        monthly_payment = principal * (monthly_rate * (1 + monthly_rate) ** num_payments) / \
                         ((1 + monthly_rate) ** num_payments - 1)
    
    return {
        "monthly_payment": round(monthly_payment, 2),
        "total_payment": round(monthly_payment * num_payments, 2),
        "total_interest": round(monthly_payment * num_payments - principal, 2)
    }

# User query that should trigger function calling
user_query = "What's the weather in Tokyo and calculate the monthly payment for a $300,000 mortgage at 4% for 30 years?"

print(f"\n👤 User: {user_query}\n")

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": user_query}],
    tools=tools,
    tool_choice="auto"  # Let model decide when to call functions
)

# Process function calls
response_message = response.choices[0].message
tool_calls = response_message.tool_calls

if tool_calls:
    print("🔧 Function Calls Detected:\n")
    
    # Execute each function call
    messages = [{"role": "user", "content": user_query}]
    messages.append(response_message)
    
    for tool_call in tool_calls:
        function_name = tool_call.function.name
        function_args = json.loads(tool_call.function.arguments)
        
        print(f"  Calling: {function_name}({function_args})")
        
        # Execute the function
        if function_name == "get_weather":
            function_response = get_weather(**function_args)
        elif function_name == "calculate_mortgage":
            function_response = calculate_mortgage(**function_args)
        
        print(f"  Result: {function_response}\n")
        
        # Add function response to messages
        messages.append({
            "tool_call_id": tool_call.id,
            "role": "tool",
            "name": function_name,
            "content": json.dumps(function_response)
        })
    
    # Get final response with function results
    final_response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )
    
    print(f"🤖 Final Response:\n{final_response.choices[0].message.content}\n")
else:
    print(f"🤖 Response:\n{response_message.content}\n")


# Example 3: JSON Mode
print("=" * 60)
print("Example 3: JSON Mode")
print("=" * 60)

response3 = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "system",
            "content": "You are a helpful assistant that outputs JSON. Extract person information."
        },
        {
            "role": "user",
            "content": "Extract info: Dr. Emily Chen, 35, works at Stanford as a Professor of Computer Science, email: emily.chen@stanford.edu"
        }
    ],
    response_format={"type": "json_object"}  # Force JSON output
)

json_output = json.loads(response3.choices[0].message.content)
print(f"\n📋 JSON Output:")
print(json.dumps(json_output, indent=2))
print()


# Example 4: Token Management
print("=" * 60)
print("Example 4: Token Usage and Management")
print("=" * 60)

response4 = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "user", "content": "Explain machine learning in 50 words."}
    ],
    max_tokens=100,  # Limit response length
    temperature=0.5
)

# Access token usage
usage = response4.usage
print(f"\n📊 Token Usage:")
print(f"  Prompt Tokens: {usage.prompt_tokens}")
print(f"  Completion Tokens: {usage.completion_tokens}")
print(f"  Total Tokens: {usage.total_tokens}")
print(f"\n🤖 Response:\n{response4.choices[0].message.content}\n")


# Example 5: Multiple Choices (n parameter)
print("=" * 60)
print("Example 5: Generating Multiple Responses")
print("=" * 60)

response5 = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "user", "content": "Generate a creative company name for an AI startup."}
    ],
    n=3,  # Generate 3 different responses
    temperature=0.9  # Higher temperature for more variety
)

print(f"\n💡 Generated {len(response5.choices)} company names:\n")
for i, choice in enumerate(response5.choices, 1):
    print(f"  {i}. {choice.message.content}")
print()


# Example 6: System Message Variations
print("=" * 60)
print("Example 6: System Message Impact")
print("=" * 60)

user_question = "What is Python?"

system_messages = [
    "You are a computer science professor.",
    "You are explaining to a 5-year-old child.",
    "You are a comedian making jokes."
]

for i, system_msg in enumerate(system_messages, 1):
    print(f"\n--- System: {system_msg} ---")
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_msg},
            {"role": "user", "content": user_question}
        ],
        temperature=0.7,
        max_tokens=100
    )
    
    print(f"🤖 {response.choices[0].message.content}\n")


# Example 7: Temperature Comparison
print("=" * 60)
print("Example 7: Temperature Effects")
print("=" * 60)

prompt = "Complete this sentence: The future of AI is"

temperatures = [0.0, 0.5, 1.0, 1.5]

for temp in temperatures:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=temp,
        max_tokens=30
    )
    
    print(f"\n🌡️  Temperature {temp}:")
    print(f"   {response.choices[0].message.content}")

print()


# Example 8: Presence and Frequency Penalties
print("=" * 60)
print("Example 8: Penalty Parameters")
print("=" * 60)

print("\n📝 Without Penalties:")
response_no_penalty = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "List 5 benefits of exercise."}],
    temperature=0.7
)
print(response_no_penalty.choices[0].message.content)

print("\n📝 With Presence Penalty (encourages topic diversity):")
response_with_penalty = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "List 5 benefits of exercise."}],
    temperature=0.7,
    presence_penalty=0.6,  # Encourage new topics
    frequency_penalty=0.3  # Reduce repetition
)
print(response_with_penalty.choices[0].message.content)
print()


# Best Practices
print("=" * 60)
print("📚 OpenAI Advanced Features - Best Practices")
print("=" * 60)
print("""
1. Streaming:
   ✅ Use for chatbots and real-time applications
   ✅ Improves perceived responsiveness
   ✅ Better user experience for long responses

2. Function Calling:
   ✅ Integrate external APIs and tools
   ✅ Validate function arguments
   ✅ Handle errors gracefully
   ✅ Use for structured actions

3. JSON Mode:
   ✅ Guarantees valid JSON output
   ✅ Must mention "JSON" in system message
   ✅ Great for data extraction

4. Token Management:
   ✅ Monitor usage for cost control
   ✅ Use max_tokens to limit responses
   ✅ Optimize prompts to reduce tokens

5. Temperature:
   ✅ 0.0-0.3: Factual, consistent responses
   ✅ 0.5-0.7: Balanced creativity
   ✅ 0.8-1.0: Creative, varied outputs
   ✅ 1.0+: Highly creative, unpredictable

6. Penalties:
   ✅ presence_penalty: Encourage new topics
   ✅ frequency_penalty: Reduce repetition
   ✅ Range: -2.0 to 2.0

Model Selection:
- gpt-4o: Most capable, multimodal
- gpt-4o-mini: Fast, cost-effective
- gpt-4-turbo: High performance
- gpt-3.5-turbo: Legacy, cheaper
""")
