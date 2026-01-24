"""
10. Structured Outputs using Pydantic
======================================
Demonstrates how to use Pydantic models to get structured, validated
outputs from LLMs.

Key Concepts:
- Pydantic BaseModel for schema definition
- Type validation and constraints
- OpenAI's structured output feature
- Parsing LLM responses into Python objects
- Error handling and validation
"""

import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel, Field, EmailStr, validator
from typing import List, Optional
from enum import Enum

load_dotenv()
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


# Example 1: Simple Person Model
print("=" * 60)
print("Example 1: Basic Pydantic Model")
print("=" * 60)

class Person(BaseModel):
    """A simple person model with validation."""
    name: str = Field(description="Full name of the person")
    age: int = Field(ge=0, le=150, description="Age in years")
    email: str = Field(description="Email address")
    occupation: str = Field(description="Current occupation")

# Show the JSON schema
print("\n📋 Pydantic Model Schema:")
print(json.dumps(Person.model_json_schema(), indent=2))

# Extract structured data from text
text1 = "My name is Alice Johnson, I'm 28 years old, my email is alice@example.com, and I work as a Data Scientist."

response1 = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": f"Extract information and return as JSON matching this schema: {Person.model_json_schema()}"},
        {"role": "user", "content": text1}
    ],
    response_format={"type": "json_object"}
)

# Parse response into Pydantic model
person_data = json.loads(response1.choices[0].message.content)
person = Person(**person_data)

print(f"\n✅ Extracted Person:")
print(f"  Name: {person.name}")
print(f"  Age: {person.age}")
print(f"  Email: {person.email}")
print(f"  Occupation: {person.occupation}\n")


# Example 2: Complex Nested Model
print("=" * 60)
print("Example 2: Nested Pydantic Models")
print("=" * 60)

class Address(BaseModel):
    """Address information."""
    street: str
    city: str
    state: str
    zip_code: str

class Company(BaseModel):
    """Company information."""
    name: str
    industry: str
    size: str  # e.g., "Small", "Medium", "Large"

class Employee(BaseModel):
    """Employee with nested models."""
    name: str
    position: str
    salary: float = Field(ge=0, description="Annual salary in USD")
    address: Address
    company: Company
    skills: List[str]

text2 = """
John Smith works as a Senior Software Engineer at TechCorp, a large technology company.
He earns $120,000 per year. He lives at 123 Main Street, San Francisco, CA 94105.
His skills include Python, JavaScript, and Docker.
"""

response2 = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": f"Extract employee information as JSON: {Employee.model_json_schema()}"},
        {"role": "user", "content": text2}
    ],
    response_format={"type": "json_object"}
)

employee_data = json.loads(response2.choices[0].message.content)
employee = Employee(**employee_data)

print(f"\n✅ Extracted Employee:")
print(f"  Name: {employee.name}")
print(f"  Position: {employee.position}")
print(f"  Salary: ${employee.salary:,.2f}")
print(f"  Address: {employee.address.street}, {employee.address.city}, {employee.address.state}")
print(f"  Company: {employee.company.name} ({employee.company.industry})")
print(f"  Skills: {', '.join(employee.skills)}\n")


# Example 3: Using Enums for Controlled Values
print("=" * 60)
print("Example 3: Enums for Controlled Outputs")
print("=" * 60)

class Sentiment(str, Enum):
    """Sentiment classification."""
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"

class Priority(str, Enum):
    """Priority levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

class CustomerFeedback(BaseModel):
    """Customer feedback analysis."""
    customer_name: str
    sentiment: Sentiment
    priority: Priority
    summary: str = Field(max_length=200)
    action_items: List[str]

feedback_text = """
Customer Sarah Williams called about a critical bug in the payment system.
She was very frustrated and needs this fixed immediately. The issue is preventing
her from processing customer orders. We need to escalate this to the dev team
and provide a hotfix within 24 hours.
"""

response3 = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": f"Analyze customer feedback as JSON: {CustomerFeedback.model_json_schema()}"},
        {"role": "user", "content": feedback_text}
    ],
    response_format={"type": "json_object"}
)

feedback_data = json.loads(response3.choices[0].message.content)
feedback = CustomerFeedback(**feedback_data)

print(f"\n✅ Feedback Analysis:")
print(f"  Customer: {feedback.customer_name}")
print(f"  Sentiment: {feedback.sentiment.value.upper()}")
print(f"  Priority: {feedback.priority.value.upper()}")
print(f"  Summary: {feedback.summary}")
print(f"  Action Items:")
for item in feedback.action_items:
    print(f"    - {item}")
print()


# Example 4: OpenAI's Native Structured Output (Beta)
print("=" * 60)
print("Example 4: OpenAI Native Structured Output")
print("=" * 60)

class CalendarEvent(BaseModel):
    """Calendar event extraction."""
    event_name: str = Field(description="Name of the event")
    date: str = Field(description="Date in YYYY-MM-DD format")
    time: str = Field(description="Time in HH:MM format")
    participants: List[str] = Field(description="List of participants")
    location: Optional[str] = Field(None, description="Event location")

event_text = "Team meeting with Alice, Bob, and Charlie on January 15th, 2026 at 2:30 PM in Conference Room A."

# Using the beta parse method for structured outputs
try:
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-2024-08-06",  # Requires specific model version
        messages=[
            {"role": "system", "content": "Extract calendar event information."},
            {"role": "user", "content": event_text}
        ],
        response_format=CalendarEvent,
    )
    
    event = completion.choices[0].message.parsed
    
    print(f"\n✅ Extracted Event (Native Structured Output):")
    print(f"  Event: {event.event_name}")
    print(f"  Date: {event.date}")
    print(f"  Time: {event.time}")
    print(f"  Participants: {', '.join(event.participants)}")
    print(f"  Location: {event.location or 'Not specified'}\n")
    
except Exception as e:
    print(f"\n⚠️  Native structured output not available: {e}")
    print("Falling back to JSON mode...\n")
    
    # Fallback to regular JSON mode
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": f"Extract event as JSON: {CalendarEvent.model_json_schema()}"},
            {"role": "user", "content": event_text}
        ],
        response_format={"type": "json_object"}
    )
    
    event_data = json.loads(response.choices[0].message.content)
    event = CalendarEvent(**event_data)
    
    print(f"✅ Extracted Event (JSON Mode):")
    print(f"  Event: {event.event_name}")
    print(f"  Date: {event.date}")
    print(f"  Time: {event.time}")
    print(f"  Participants: {', '.join(event.participants)}")
    print(f"  Location: {event.location or 'Not specified'}\n")


# Example 5: List of Objects
print("=" * 60)
print("Example 5: Extracting Multiple Items")
print("=" * 60)

class Product(BaseModel):
    """Product information."""
    name: str
    price: float
    category: str
    in_stock: bool

class ShoppingList(BaseModel):
    """List of products."""
    items: List[Product]
    total_items: int

shopping_text = """
I need to buy:
1. iPhone 15 Pro - $999 (Electronics) - In stock
2. Nike Running Shoes - $120 (Sports) - Out of stock
3. Python Programming Book - $45 (Books) - In stock
4. Wireless Headphones - $79 (Electronics) - In stock
"""

response5 = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": f"Extract shopping list as JSON: {ShoppingList.model_json_schema()}"},
        {"role": "user", "content": shopping_text}
    ],
    response_format={"type": "json_object"}
)

shopping_data = json.loads(response5.choices[0].message.content)
shopping_list = ShoppingList(**shopping_data)

print(f"\n✅ Shopping List ({shopping_list.total_items} items):")
for i, product in enumerate(shopping_list.items, 1):
    stock_status = "✓ In Stock" if product.in_stock else "✗ Out of Stock"
    print(f"  {i}. {product.name} - ${product.price} ({product.category}) - {stock_status}")
print()


# Example 6: Custom Validators
print("=" * 60)
print("Example 6: Custom Validation")
print("=" * 60)

class ValidatedPerson(BaseModel):
    """Person with custom validation."""
    name: str
    age: int
    email: str
    phone: str
    
    @validator('name')
    def name_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('Name cannot be empty')
        return v.title()  # Capitalize
    
    @validator('age')
    def age_must_be_reasonable(cls, v):
        if v < 0 or v > 150:
            raise ValueError('Age must be between 0 and 150')
        return v
    
    @validator('email')
    def email_must_be_valid(cls, v):
        if '@' not in v:
            raise ValueError('Invalid email format')
        return v.lower()

# Test with valid data
try:
    valid_person = ValidatedPerson(
        name="john doe",
        age=30,
        email="JOHN@EXAMPLE.COM",
        phone="555-1234"
    )
    print(f"\n✅ Valid Person Created:")
    print(f"  Name: {valid_person.name}")  # Will be capitalized
    print(f"  Age: {valid_person.age}")
    print(f"  Email: {valid_person.email}")  # Will be lowercase
    print(f"  Phone: {valid_person.phone}")
except Exception as e:
    print(f"\n❌ Validation Error: {e}")

# Test with invalid data
try:
    invalid_person = ValidatedPerson(
        name="",
        age=200,
        email="invalid-email",
        phone="555-1234"
    )
except Exception as e:
    print(f"\n❌ Validation Error (Expected): {e}\n")


# Best Practices
print("=" * 60)
print("📚 Pydantic Best Practices")
print("=" * 60)
print("""
1. ✅ Clear Field Descriptions: Help the LLM understand what to extract
2. ✅ Type Constraints: Use Field() with ge, le, max_length, etc.
3. ✅ Optional Fields: Use Optional[] for fields that might be missing
4. ✅ Enums: Use for controlled vocabularies
5. ✅ Nested Models: Break complex structures into smaller models
6. ✅ Validators: Add custom validation logic
7. ✅ Default Values: Provide sensible defaults

Benefits of Structured Outputs:
- Type safety and validation
- Automatic parsing and error handling
- Clear schema definition
- Easy integration with databases
- Self-documenting code

Use Cases:
- Data extraction from text
- Form validation
- API response parsing
- Database model mapping
- Configuration management
""")


# Comparison: Unstructured vs Structured
print("=" * 60)
print("📊 Unstructured vs Structured Comparison")
print("=" * 60)

print("\n❌ Unstructured Output:")
unstructured_response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "user", "content": "Extract name and age from: Bob is 25 years old"}
    ]
)
print(f"  {unstructured_response.choices[0].message.content}")
print("  → Requires manual parsing, no validation, inconsistent format")

print("\n✅ Structured Output:")
class SimpleExtraction(BaseModel):
    name: str
    age: int

structured_response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": f"Extract as JSON: {SimpleExtraction.model_json_schema()}"},
        {"role": "user", "content": "Extract name and age from: Bob is 25 years old"}
    ],
    response_format={"type": "json_object"}
)

data = json.loads(structured_response.choices[0].message.content)
extraction = SimpleExtraction(**data)
print(f"  Name: {extraction.name}, Age: {extraction.age}")
print("  → Automatic parsing, type validation, consistent format\n")
