"""
RAG INDEXING SCRIPT
===================
This script indexes a PDF document into a vector database for Retrieval-Augmented Generation (RAG).

Process:
1. Load PDF document
2. Split into smaller chunks
3. Convert chunks to embeddings
4. Store in Qdrant vector database

Dependencies:
- python-dotenv: Load environment variables from .env file
- langchain-community: Community integrations (PDF loader)
- langchain-text-splitters: Text splitting utilities
- langchain-openai: OpenAI integration for embeddings
- langchain-qdrant: Qdrant vector store integration
- pypdf: PDF parsing library (used by PyPDFLoader)
"""

# ============================================================================
# IMPORTS
# ============================================================================

# dotenv: Loads environment variables from .env file (e.g., OPENAI_API_KEY)
from dotenv import load_dotenv

# pathlib: Modern way to handle file paths in Python
from pathlib import Path

# PyPDFLoader: LangChain's PDF document loader
# Extracts text from PDF files page by page
from langchain_community.document_loaders import PyPDFLoader

# RecursiveCharacterTextSplitter: Intelligently splits text into chunks
# Uses recursive splitting to maintain semantic coherence
from langchain_text_splitters import RecursiveCharacterTextSplitter

# OpenAIEmbeddings: Converts text to vector embeddings using OpenAI's API
# Embeddings are numerical representations that capture semantic meaning
from langchain_openai import OpenAIEmbeddings

# QdrantVectorStore: Interface to Qdrant vector database
# Stores and retrieves document embeddings for similarity search
from langchain_qdrant import QdrantVectorStore

# ============================================================================
# CONFIGURATION
# ============================================================================

# Load environment variables (OPENAI_API_KEY)
load_dotenv()

# Get the path to the PDF file in the same directory as this script
pdf_path = Path(__file__).parent / "nodejs.pdf"

# ============================================================================
# STEP 1: LOAD PDF DOCUMENT
# ============================================================================

# Initialize PDF loader with the file path
# PyPDFLoader will extract text from each page of the PDF
loader = PyPDFLoader(file_path=str(pdf_path))

# Load the document - returns a list of Document objects (one per page)
# Each Document has: page_content (text) and metadata (page number, source)
docs = loader.load()

# ============================================================================
# STEP 2: SPLIT DOCUMENTS INTO CHUNKS
# ============================================================================

# Create a text splitter with specific parameters
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,        # Maximum characters per chunk
    chunk_overlap=400       # Overlap between chunks to maintain context
)

# Why chunking?
# - LLMs have token limits
# - Smaller chunks = more precise retrieval
# - Overlap ensures context isn't lost at boundaries

# Split all documents into smaller chunks
chunks = text_splitter.split_documents(documents=docs)

# ============================================================================
# STEP 3: CREATE EMBEDDING MODEL
# ============================================================================

# Initialize OpenAI's embedding model
# text-embedding-3-large: Latest, most powerful embedding model
# - Produces 3072-dimensional vectors
# - Better semantic understanding than older models
embedding_model = OpenAIEmbeddings(
    model="text-embedding-3-large"
)

# ============================================================================
# STEP 4: STORE IN VECTOR DATABASE
# ============================================================================

# Create Qdrant vector store from documents
# This will:
# 1. Convert each chunk to embeddings using OpenAI
# 2. Store embeddings in Qdrant at localhost:6333
# 3. Create a collection named "learning-rag"
vector_store = QdrantVectorStore.from_documents(
    documents=chunks,                   # Text chunks to embed
    embedding=embedding_model,          # Embedding model to use
    url="http://localhost:6333",        # Qdrant server URL
    collection_name="learning-rag"      # Collection name in Qdrant
)

print("✅ Indexing of Documents done...")
print(f"📊 Indexed {len(chunks)} chunks from {len(docs)} pages")
