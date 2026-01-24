"""
RAG CHAT INTERFACE
==================
This script provides an interactive chat interface for querying the indexed documents.

Process:
1. Connect to existing Qdrant vector database
2. Accept user query
3. Retrieve relevant chunks using similarity search
4. Generate answer using OpenAI with retrieved context

Dependencies:
- python-dotenv: Load environment variables from .env file
- langchain-openai: OpenAI integration for embeddings
- langchain-qdrant: Qdrant vector store integration
- openai: Direct OpenAI API client for chat completions
"""

# ============================================================================
# IMPORTS
# ============================================================================

# dotenv: Loads environment variables from .env file (e.g., OPENAI_API_KEY)
from dotenv import load_dotenv

# OpenAIEmbeddings: Converts text to vector embeddings using OpenAI's API
# Used to embed the user's query for similarity search
from langchain_openai import OpenAIEmbeddings

# QdrantVectorStore: Interface to Qdrant vector database
# Retrieves similar documents based on query embeddings
from langchain_qdrant import QdrantVectorStore

# OpenAI: Direct API client for chat completions
# Used to generate final answers using GPT models
from openai import OpenAI

# ============================================================================
# CONFIGURATION
# ============================================================================

# Load environment variables (OPENAI_API_KEY)
load_dotenv()

# Initialize OpenAI client for chat completions
openai_client = OpenAI()

# ============================================================================
# STEP 1: CONNECT TO VECTOR DATABASE
# ============================================================================

# Initialize the same embedding model used during indexing
# IMPORTANT: Must use the same model to ensure vector compatibility
embedding_model = OpenAIEmbeddings(
    model="text-embedding-3-large"
)

# Connect to existing Qdrant collection
# This doesn't re-index, just connects to the already-indexed data
vector_db = QdrantVectorStore.from_existing_collection(
    url="http://localhost:6333",        # Qdrant server URL
    collection_name="learning-rag",     # Collection created by index.py
    embedding=embedding_model,          # Embedding model for queries
)

# ============================================================================
# STEP 2: GET USER QUERY
# ============================================================================

# Prompt user for their question
user_query = input("Ask Something ... ")

# ============================================================================
# STEP 3: RETRIEVE RELEVANT CHUNKS (RETRIEVAL)
# ============================================================================

# Perform similarity search in the vector database
# This finds the most semantically similar chunks to the user's query
# Returns top 4 most relevant chunks by default
search_results = vector_db.similarity_search(query=user_query)

# Format the retrieved chunks into context for the LLM
# Each result includes:
# - page_content: The actual text chunk
# - metadata: Page number and source file
context = "\n\n\n".join([
    f"Page Content: {result.page_content}\n"
    f"Page Number: {result.metadata['page_label']}\n"
    f"File Location: {result.metadata['source']}"
    for result in search_results
])

# ============================================================================
# STEP 4: GENERATE ANSWER (AUGMENTED GENERATION)
# ============================================================================

# Define the system prompt template
# This instructs the AI on how to use the retrieved context
SYSTEM_PROMPT_TEMPLATE = """
    You are a helpful AI Assistant who answers user queries based on the available context
    retrieved from a PDF file along with page contents and page numbers.

    You should only answer the user based on the following context and navigate the user
    to open the right page number to know more.

    context:{context}
"""

# Format the prompt with the actual retrieved context
final_system_prompt = SYSTEM_PROMPT_TEMPLATE.format(context=context)

# Call OpenAI's chat completion API
# This generates the final answer using the retrieved context
response = openai_client.chat.completions.create(
    model="gpt-4o",  # GPT-4 Optimized model (fast and powerful)
    messages=[
        {"role": "system", "content": final_system_prompt},  # System instructions + context
        {"role": "user", "content": user_query}              # User's question
    ]
)

# ============================================================================
# STEP 5: DISPLAY ANSWER
# ============================================================================

# Extract and print the AI's response
print(f"\n🤖 Bot: {response.choices[0].message.content}")