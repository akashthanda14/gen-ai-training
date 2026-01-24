"""
Module 2: Structured Outputs using Pydantic + Instructor
=========================================================
Move beyond parsing messy strings. Force LLMs to speak "Code" (JSON)
instead of "English."

The Problem: LLMs return strings like "Here is your JSON: {...}"
The Solution: instructor library - the industry standard

Key Concept: response_model parameter gives you TYPED Python objects
"""

import os
from dotenv import load_dotenv
from openai import OpenAI
import instructor
from pydantic import BaseModel, Field
from typing import List

load_dotenv()

# ============================================================================
# Step 1: Patch the OpenAI client with instructor
# ============================================================================

# Regular OpenAI client
regular_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Patched client with instructor (adds response_model support)
client = instructor.from_openai(regular_client)


# ============================================================================
# Example 1: The Problem - Manual String Parsing
# ============================================================================

print("=" * 70)
print("Example 1: The Problem with Manual Parsing")
print("=" * 70)

print("\n❌ WITHOUT INSTRUCTOR (Manual Parsing):")
print("-" * 70)

# Ask for JSON without instructor
response_manual = regular_client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "Extract user info and return as JSON."},
        {"role": "user", "content": "John is a 25 year old Python developer."}
    ],
    temperature=0.1
)

raw_text = response_manual.choices[0].message.content
print(f"Raw response:\n{raw_text}\n")

print("⚠️  PROBLEMS:")
print("1. Response might have extra text: 'Here is your JSON: {...}'")
print("2. No type safety - could be any structure")
print("3. No validation - fields might be missing")
print("4. Need manual JSON parsing and error handling")
print()


# ============================================================================
# Example 2: The Solution - Instructor with Pydantic
# ============================================================================

print("=" * 70)
print("Example 2: The Solution with Instructor")
print("=" * 70)

# Step 1: Define the desired structure with Pydantic
class UserInfo(BaseModel):
    """User information model."""
    name: str = Field(description="Full name of the person")
    age: int = Field(description="Age in years")
    is_developer: bool = Field(description="Whether the person is a developer")


print("\n✅ WITH INSTRUCTOR (Type-Safe):")
print("-" * 70)

# Step 2: Use response_model parameter
user = client.chat.completions.create(
    model="gpt-4o-mini",
    response_model=UserInfo,  # <--- THE MAGIC!
    messages=[
        {"role": "user", "content": "John is a 25 year old Python developer."}
    ]
)

# Step 3: Get typed Python object
print(f"Type: {type(user)}")  # <class 'UserInfo'>
print(f"Name: {user.name} (type: {type(user.name).__name__})")
print(f"Age: {user.age} (type: {type(user.age).__name__})")
print(f"Is Developer: {user.is_developer} (type: {type(user.is_developer).__name__})")

print("\n✅ BENEFITS:")
print("1. Guaranteed valid structure")
print("2. Type safety (IDE autocomplete works!)")
print("3. Automatic validation")
print("4. No manual parsing needed")
print()


# ============================================================================
# Example 3: Complex Nested Structures
# ============================================================================

print("=" * 70)
print("Example 3: Complex Nested Structures")
print("=" * 70)

class Address(BaseModel):
    """Address information."""
    street: str
    city: str
    country: str


class Company(BaseModel):
    """Company information."""
    name: str
    industry: str


class Employee(BaseModel):
    """Employee with nested models."""
    name: str
    position: str
    salary: float = Field(ge=0, description="Annual salary in USD")
    address: Address
    company: Company
    skills: List[str]


text = """
Sarah Johnson works as a Senior Software Engineer at TechCorp, a technology company.
She earns $120,000 per year. She lives at 123 Main Street in San Francisco, USA.
Her skills include Python, JavaScript, and Docker.
"""

print(f"\n📝 Input Text:\n{text}")

employee = client.chat.completions.create(
    model="gpt-4o-mini",
    response_model=Employee,
    messages=[
        {"role": "user", "content": f"Extract employee information from: {text}"}
    ]
)

print("\n✅ Extracted Employee (Nested Structure):")
print(f"  Name: {employee.name}")
print(f"  Position: {employee.position}")
print(f"  Salary: ${employee.salary:,.2f}")
print(f"  Address: {employee.address.street}, {employee.address.city}, {employee.address.country}")
print(f"  Company: {employee.company.name} ({employee.company.industry})")
print(f"  Skills: {', '.join(employee.skills)}")
print()


# ============================================================================
# Example 4: Lists of Objects
# ============================================================================

print("=" * 70)
print("Example 4: Extracting Multiple Items")
print("=" * 70)

class Product(BaseModel):
    """Product information."""
    name: str
    price: float
    in_stock: bool


class ShoppingList(BaseModel):
    """List of products."""
    items: List[Product]


shopping_text = """
I need to buy:
1. iPhone 15 Pro - $999 - In stock
2. Nike Running Shoes - $120 - Out of stock
3. Wireless Headphones - $79 - In stock
"""

print(f"\n📝 Input Text:\n{shopping_text}")

shopping_list = client.chat.completions.create(
    model="gpt-4o-mini",
    response_model=ShoppingList,
    messages=[
        {"role": "user", "content": f"Extract shopping list from: {shopping_text}"}
    ]
)

print(f"\n✅ Extracted Shopping List ({len(shopping_list.items)} items):")
for i, product in enumerate(shopping_list.items, 1):
    stock_status = "✓ In Stock" if product.in_stock else "✗ Out of Stock"
    print(f"  {i}. {product.name} - ${product.price} - {stock_status}")
print()


# ============================================================================
# Example 5: Validation with Field Constraints
# ============================================================================

print("=" * 70)
print("Example 5: Automatic Validation")
print("=" * 70)

from pydantic import validator, EmailStr

class ValidatedUser(BaseModel):
    """User with validation rules."""
    name: str = Field(min_length=1, max_length=100)
    age: int = Field(ge=0, le=150, description="Age must be 0-150")
    email: EmailStr  # Validates email format
    
    @validator('name')
    def name_must_be_capitalized(cls, v):
        """Ensure name is capitalized."""
        return v.title()


print("\n📝 Input: 'alice smith is 30 years old, email: alice@example.com'")

validated_user = client.chat.completions.create(
    model="gpt-4o-mini",
    response_model=ValidatedUser,
    messages=[
        {"role": "user", "content": "alice smith is 30 years old, email: alice@example.com"}
    ]
)

print(f"\n✅ Validated User:")
print(f"  Name: {validated_user.name} (automatically capitalized!)")
print(f"  Age: {validated_user.age} (validated: 0-150)")
print(f"  Email: {validated_user.email} (validated format)")
print()


# ============================================================================
# Example 6: Comparison - Before and After
# ============================================================================

print("=" * 70)
print("Example 6: Side-by-Side Comparison")
print("=" * 70)

task = "Extract: Bob is 28, lives in NYC, works as a data scientist"

print("\n1️⃣  MANUAL APPROACH (Without Instructor):")
print("-" * 70)

import json

response_manual = regular_client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "Extract as JSON with fields: name, age, city, job"},
        {"role": "user", "content": task}
    ],
    response_format={"type": "json_object"}
)

manual_text = response_manual.choices[0].message.content
print(f"Response: {manual_text}")

try:
    manual_data = json.loads(manual_text)
    print(f"Parsed: {manual_data}")
    print(f"Type: {type(manual_data)} (just a dict!)")
    print(f"Name type: {type(manual_data.get('name'))} (could be None!)")
except json.JSONDecodeError as e:
    print(f"❌ JSON parsing failed: {e}")

print("\n2️⃣  INSTRUCTOR APPROACH (Type-Safe):")
print("-" * 70)

class Person(BaseModel):
    name: str
    age: int
    city: str
    job: str


person = client.chat.completions.create(
    model="gpt-4o-mini",
    response_model=Person,
    messages=[{"role": "user", "content": task}]
)

print(f"Response: {person}")
print(f"Type: {type(person)} (Person object!)")
print(f"Name: {person.name} (type: {type(person.name).__name__})")
print(f"Age: {person.age} (type: {type(person.age).__name__})")

print("\n💡 NOTICE:")
print("- Instructor gives you a TYPED object")
print("- IDE autocomplete works!")
print("- No manual parsing needed")
print("- Validation is automatic")
print()


# ============================================================================
# Teaching Points
# ============================================================================

print("=" * 70)
print("🎓 KEY TEACHING POINTS")
print("=" * 70)

print("""
1. THE PROBLEM WITH STRINGS
   -------------------------
   LLMs return text. Even with JSON mode, you get:
   - A string that might not be valid JSON
   - No type information
   - No validation
   - Manual parsing required

2. PYDANTIC MODELS
   ----------------
   Define your desired structure:
   
   class UserInfo(BaseModel):
       name: str
       age: int
   
   This is like a "contract" - the LLM MUST return this structure.

3. INSTRUCTOR MAGIC
   -----------------
   client = instructor.from_openai(OpenAI())
   
   This patches the client to add response_model parameter.
   Behind the scenes, instructor:
   - Converts your Pydantic model to a JSON schema
   - Tells the LLM to follow that schema
   - Validates the response
   - Retries if validation fails
   - Returns a typed Python object

4. TYPE SAFETY
   ------------
   user = client.chat.completions.create(
       response_model=UserInfo,
       ...
   )
   
   Now 'user' is a UserInfo object, not a string!
   - user.name is guaranteed to be a string
   - user.age is guaranteed to be an int
   - IDE autocomplete works
   - Type checkers (mypy) work

5. AUTOMATIC VALIDATION
   ---------------------
   class User(BaseModel):
       age: int = Field(ge=0, le=150)
   
   If the LLM returns age=-5, Pydantic raises an error.
   Instructor automatically retries with the error message!

6. NESTED STRUCTURES
   ------------------
   You can nest Pydantic models:
   
   class Address(BaseModel):
       street: str
       city: str
   
   class Person(BaseModel):
       name: str
       address: Address  # Nested!
   
   Instructor handles this automatically.

7. LISTS AND ARRAYS
   -----------------
   class ShoppingList(BaseModel):
       items: List[Product]
   
   Extract multiple items in one call!

8. WHEN TO USE INSTRUCTOR
   -----------------------
   ✅ Data extraction from text
   ✅ Structured API responses
   ✅ Form validation
   ✅ Database model population
   ✅ Type-safe LLM interactions
   
   ❌ Simple text generation (overkill)
   ❌ Creative writing (too restrictive)

9. COMPARISON TO ALTERNATIVES
   ---------------------------
   Manual JSON parsing: Error-prone, no types
   JSON mode: Better, but still strings
   Function calling: Complex, limited
   Instructor: Best of all worlds!

10. INDUSTRY STANDARD
    ------------------
    instructor is used by:
    - Startups building AI products
    - Enterprise applications
    - Production systems
    
    It's the de facto standard for structured LLM outputs.
""")


print("\n" + "=" * 70)
print("✅ Module 2 - Basic Instructor Complete!")
print("=" * 70)
print("\nNext: Run advanced_validation.py for complex examples")
print("\nThen move to Module 3: Running & Using LLMs!")
