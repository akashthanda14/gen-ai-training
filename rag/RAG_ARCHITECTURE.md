# RAG System Architecture & Documentation

## 📚 Table of Contents
1. [Overview](#overview)
2. [System Architecture](#system-architecture)
3. [Components Deep Dive](#components-deep-dive)
4. [Flow Diagrams](#flow-diagrams)
5. [Technical Notes](#technical-notes)
6. [Setup & Usage](#setup--usage)
7. [Best Practices](#best-practices)

---

## Overview

**RAG (Retrieval-Augmented Generation)** is a technique that enhances Large Language Models (LLMs) by providing them with relevant external knowledge retrieved from a document database. This system implements RAG for querying PDF documents using:

- **Vector Database**: Qdrant
- **Embeddings**: OpenAI text-embedding-3-large
- **LLM**: GPT-4o
- **Framework**: LangChain

### Why RAG?

| Problem | RAG Solution |
|---------|--------------|
| LLMs have knowledge cutoff dates | Provides up-to-date information from your documents |
| LLMs can hallucinate | Grounds responses in actual document content |
| Limited context window | Retrieves only relevant chunks instead of entire documents |
| Domain-specific knowledge | Enables querying private/specialized documents |

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         RAG SYSTEM ARCHITECTURE                      │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│                        PHASE 1: INDEXING                             │
│                         (index.py)                                   │
└─────────────────────────────────────────────────────────────────────┘

    ┌──────────────┐
    │  nodejs.pdf  │  ← Source Document
    └──────┬───────┘
           │
           ▼
    ┌──────────────────┐
    │  PyPDFLoader     │  ← Extract text from PDF
    │  (LangChain)     │
    └──────┬───────────┘
           │
           ▼
    ┌──────────────────────────────────────┐
    │  Raw Document Pages                  │
    │  • Page 1: "Node.js is..."           │
    │  • Page 2: "Event loop..."           │
    │  • Page 3: "Modules..."              │
    └──────┬───────────────────────────────┘
           │
           ▼
    ┌──────────────────────────────────────┐
    │  RecursiveCharacterTextSplitter      │  ← Split into chunks
    │  • chunk_size: 1000 chars            │
    │  • chunk_overlap: 400 chars          │
    └──────┬───────────────────────────────┘
           │
           ▼
    ┌──────────────────────────────────────┐
    │  Text Chunks (with metadata)         │
    │  Chunk 1: "Node.js is a..."          │
    │  Chunk 2: "...runtime built on..."   │
    │  Chunk 3: "...Chrome's V8 engine..." │
    └──────┬───────────────────────────────┘
           │
           ▼
    ┌──────────────────────────────────────┐
    │  OpenAI Embeddings API               │  ← Convert to vectors
    │  Model: text-embedding-3-large       │
    │  Dimensions: 3072                    │
    └──────┬───────────────────────────────┘
           │
           ▼
    ┌──────────────────────────────────────┐
    │  Vector Embeddings                   │
    │  [0.234, -0.891, 0.456, ...]        │
    │  [0.123, 0.567, -0.234, ...]        │
    │  [-0.456, 0.789, 0.123, ...]        │
    └──────┬───────────────────────────────┘
           │
           ▼
    ┌──────────────────────────────────────┐
    │  Qdrant Vector Database              │  ← Store vectors
    │  Collection: "learning-rag"          │
    │  URL: http://localhost:6333          │
    │  • Vectors + Metadata + Text         │
    └──────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────────┐
│                      PHASE 2: QUERYING                               │
│                        (chat.py)                                     │
└─────────────────────────────────────────────────────────────────────┘

    ┌──────────────────┐
    │  User Query      │  ← "What is the event loop in Node.js?"
    └──────┬───────────┘
           │
           ▼
    ┌──────────────────────────────────────┐
    │  OpenAI Embeddings API               │  ← Convert query to vector
    │  Model: text-embedding-3-large       │
    └──────┬───────────────────────────────┘
           │
           ▼
    ┌──────────────────────────────────────┐
    │  Query Vector                        │
    │  [0.345, -0.678, 0.912, ...]        │
    └──────┬───────────────────────────────┘
           │
           ▼
    ┌──────────────────────────────────────┐
    │  Qdrant Vector Database              │  ← Similarity search
    │  • Cosine similarity                 │
    │  • Returns top 4 chunks              │
    └──────┬───────────────────────────────┘
           │
           ▼
    ┌──────────────────────────────────────┐
    │  Retrieved Context                   │
    │  • Chunk: "The event loop is..."     │
    │  • Page: 15                          │
    │  • Source: nodejs.pdf                │
    └──────┬───────────────────────────────┘
           │
           ▼
    ┌──────────────────────────────────────┐
    │  Prompt Construction                 │
    │  System: "Answer based on context"   │
    │  Context: [Retrieved chunks]         │
    │  User: [Original query]              │
    └──────┬───────────────────────────────┘
           │
           ▼
    ┌──────────────────────────────────────┐
    │  OpenAI Chat Completion              │  ← Generate answer
    │  Model: gpt-4o                       │
    └──────┬───────────────────────────────┘
           │
           ▼
    ┌──────────────────────────────────────┐
    │  Final Answer                        │
    │  "The event loop in Node.js is a     │
    │   mechanism that handles async...    │
    │   See page 15 for more details."     │
    └──────────────────────────────────────┘
```

---

## Components Deep Dive

### 1. **Document Loading** (`PyPDFLoader`)

**Purpose**: Extract text from PDF files

**How it works**:
- Reads PDF file page by page
- Extracts text content from each page
- Creates Document objects with metadata

**Output**:
```python
[
    Document(
        page_content="Node.js is a JavaScript runtime...",
        metadata={"page": 0, "source": "nodejs.pdf"}
    ),
    Document(
        page_content="The event loop is...",
        metadata={"page": 1, "source": "nodejs.pdf"}
    )
]
```

---

### 2. **Text Splitting** (`RecursiveCharacterTextSplitter`)

**Purpose**: Break large documents into manageable chunks

**Configuration**:
- `chunk_size=1000`: Maximum 1000 characters per chunk
- `chunk_overlap=400`: 400 characters overlap between chunks

**Why overlap?**
- Prevents context loss at chunk boundaries
- Ensures complete sentences/paragraphs aren't split awkwardly
- Improves retrieval quality

**Example**:
```
Document: "Node.js is a runtime. It uses V8 engine. The event loop handles async operations."

Chunk 1: "Node.js is a runtime. It uses V8 engine. The event..."
Chunk 2: "...V8 engine. The event loop handles async operations."
         └─────────┘
         Overlap region
```

---

### 3. **Embeddings** (`OpenAIEmbeddings`)

**Purpose**: Convert text to numerical vectors that capture semantic meaning

**Model**: `text-embedding-3-large`
- **Dimensions**: 3072
- **Advantages**: 
  - Better semantic understanding
  - Captures nuanced meanings
  - Multilingual support

**How it works**:
```
Text: "Node.js is fast"
  ↓
Embedding API
  ↓
Vector: [0.234, -0.891, 0.456, ..., 0.123]  (3072 dimensions)
```

**Key Concept**: Similar texts have similar vectors
```
"Node.js is fast"     → [0.2, 0.8, ...]
"Node.js is quick"    → [0.21, 0.79, ...]  ← Very similar!
"Python is slow"      → [-0.5, -0.3, ...]  ← Different!
```

---

### 4. **Vector Database** (`Qdrant`)

**Purpose**: Store and search embeddings efficiently

**Why Qdrant?**
- ✅ Fast similarity search
- ✅ Scalable (millions of vectors)
- ✅ Open-source
- ✅ Easy Docker deployment
- ✅ Supports filtering and metadata

**Storage Structure**:
```
Collection: "learning-rag"
├── Point 1
│   ├── Vector: [0.234, -0.891, ...]
│   ├── Payload: {
│   │     "page_content": "Node.js is...",
│   │     "page_label": "1",
│   │     "source": "nodejs.pdf"
│   │   }
├── Point 2
│   ├── Vector: [0.123, 0.567, ...]
│   └── Payload: {...}
```

**Similarity Search**:
- Uses **cosine similarity** to find nearest vectors
- Returns top-k most similar chunks
- Includes both vectors and metadata

---

### 5. **LLM Generation** (`GPT-4o`)

**Purpose**: Generate human-like answers using retrieved context

**Prompt Structure**:
```
System: "You are a helpful AI Assistant who answers based on context..."
Context: [Retrieved chunks with page numbers]
User: "What is the event loop?"
  ↓
GPT-4o processes and generates answer
  ↓
Answer: "The event loop in Node.js is... (See page 15)"
```

**Why GPT-4o?**
- Fast inference
- Strong reasoning
- Good at following instructions
- Handles long contexts well

---

## Flow Diagrams

### **Indexing Flow** (One-time setup)

```
START
  │
  ├─→ Load PDF document
  │     │
  │     ├─→ Extract text page by page
  │     │
  │     └─→ Create Document objects
  │
  ├─→ Split documents into chunks
  │     │
  │     ├─→ Apply chunk_size=1000
  │     │
  │     └─→ Apply chunk_overlap=400
  │
  ├─→ Generate embeddings
  │     │
  │     ├─→ For each chunk
  │     │     │
  │     │     └─→ Call OpenAI API
  │     │           │
  │     │           └─→ Get 3072-dim vector
  │     │
  │     └─→ Collect all vectors
  │
  └─→ Store in Qdrant
        │
        ├─→ Create collection "learning-rag"
        │
        ├─→ Insert vectors + metadata
        │
        └─→ Index for fast search
          │
          └─→ END (Ready for queries!)
```

---

### **Query Flow** (Every user question)

```
START
  │
  ├─→ User enters query
  │     │
  │     └─→ "What is the event loop?"
  │
  ├─→ Convert query to embedding
  │     │
  │     └─→ Call OpenAI API
  │           │
  │           └─→ Get query vector
  │
  ├─→ Search vector database
  │     │
  │     ├─→ Calculate similarity scores
  │     │     │
  │     │     └─→ Cosine similarity with all stored vectors
  │     │
  │     └─→ Retrieve top 4 chunks
  │           │
  │           └─→ Include page numbers & source
  │
  ├─→ Build context
  │     │
  │     └─→ Format retrieved chunks
  │           │
  │           └─→ "Page Content: ...\nPage Number: 15\n..."
  │
  ├─→ Create prompt
  │     │
  │     ├─→ System: Instructions
  │     │
  │     ├─→ Context: Retrieved chunks
  │     │
  │     └─→ User: Original query
  │
  ├─→ Call GPT-4o
  │     │
  │     └─→ Generate answer based on context
  │
  └─→ Display answer to user
        │
        └─→ END
```

---

### **Data Flow Diagram**

```
┌─────────────┐
│   PDF File  │
└──────┬──────┘
       │
       ▼
┌─────────────────┐
│  Text Chunks    │ ←─────────┐
└──────┬──────────┘            │
       │                       │
       ▼                       │
┌─────────────────┐            │
│  Embeddings     │            │
│  (Vectors)      │            │
└──────┬──────────┘            │
       │                       │
       ▼                       │
┌─────────────────┐            │
│  Qdrant DB      │            │
│  (Storage)      │            │
└──────┬──────────┘            │
       │                       │
       │  ┌──────────────┐     │
       │  │ User Query   │     │
       │  └──────┬───────┘     │
       │         │             │
       │         ▼             │
       │  ┌──────────────┐     │
       │  │ Query Vector │     │
       │  └──────┬───────┘     │
       │         │             │
       ▼         ▼             │
┌──────────────────────┐       │
│  Similarity Search   │       │
└──────┬───────────────┘       │
       │                       │
       ▼                       │
┌──────────────────────┐       │
│  Retrieved Chunks    │───────┘
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│  Context + Query     │
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│  GPT-4o Generation   │
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│  Final Answer        │
└──────────────────────┘
```

---

## Technical Notes

### **Vector Embeddings Explained**

**What are embeddings?**
- Numerical representations of text
- Capture semantic meaning
- Enable mathematical operations on text

**Example**:
```python
# Text
text1 = "Node.js is fast"
text2 = "Node.js is quick"
text3 = "Python is slow"

# Embeddings (simplified to 3D for illustration)
vec1 = [0.8, 0.9, 0.1]
vec2 = [0.79, 0.88, 0.12]  # Similar to vec1
vec3 = [-0.5, -0.3, 0.7]   # Different from vec1

# Similarity (cosine similarity)
similarity(vec1, vec2) = 0.99  # Very similar!
similarity(vec1, vec3) = 0.12  # Not similar
```

---

### **Chunking Strategy**

**Why chunk?**
1. **Token limits**: LLMs have max context windows
2. **Precision**: Smaller chunks = more precise retrieval
3. **Cost**: Only process relevant chunks, not entire document

**Optimal chunk size**:
- Too small → Loss of context
- Too large → Irrelevant information included
- **Sweet spot**: 500-1500 characters

**Our configuration**:
```python
chunk_size = 1000      # Good balance
chunk_overlap = 400    # 40% overlap prevents context loss
```

---

### **Similarity Search**

**How it works**:
1. Convert query to vector
2. Calculate distance to all stored vectors
3. Return nearest neighbors

**Distance metrics**:
- **Cosine Similarity** (used here): Measures angle between vectors
- **Euclidean Distance**: Straight-line distance
- **Dot Product**: Inner product of vectors

**Cosine Similarity Formula**:
```
similarity(A, B) = (A · B) / (||A|| × ||B||)

Range: -1 to 1
  1  = Identical
  0  = Orthogonal (unrelated)
 -1  = Opposite
```

---

### **Prompt Engineering**

**System Prompt Design**:
```python
SYSTEM_PROMPT = """
You are a helpful AI Assistant who answers user queries based on the available context
retrieved from a PDF file along with page contents and page numbers.

You should only answer the user based on the following context and navigate the user
to open the right page number to know more.

context:{context}
"""
```

**Key elements**:
1. **Role definition**: "helpful AI Assistant"
2. **Constraint**: "only answer based on context"
3. **Guidance**: "navigate to page number"
4. **Context injection**: `{context}` placeholder

---

### **Error Handling & Edge Cases**

**Common issues**:

1. **No relevant chunks found**
   - Solution: Lower similarity threshold
   - Or: Expand search to top-k results

2. **Qdrant not running**
   - Error: Connection refused
   - Solution: Start Docker container

3. **API key issues**
   - Error: Authentication failed
   - Solution: Check `.env` file

4. **Empty PDF**
   - Error: No chunks created
   - Solution: Validate PDF has extractable text

---

## Setup & Usage

### **Prerequisites**

```bash
# Python packages
pip install python-dotenv
pip install langchain-community
pip install langchain-text-splitters
pip install langchain-openai
pip install langchain-qdrant
pip install pypdf
pip install openai

# Docker (for Qdrant)
docker --version
```

---

### **Step 1: Start Qdrant**

```bash
# Navigate to RAG directory
cd /Users/work/Desktop/LLM/GEN-AI/prompts/rag

# Start Qdrant using Docker Compose
docker-compose up -d

# Verify it's running
curl http://localhost:6333/health
# Should return: {"status":"ok"}
```

---

### **Step 2: Configure Environment**

```bash
# Create .env file
cat > .env << EOF
OPENAI_API_KEY=your_openai_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
EOF
```

---

### **Step 3: Index Documents**

```bash
# Run indexing script
python index.py

# Expected output:
# ✅ Indexing of Documents done...
# 📊 Indexed 127 chunks from 42 pages
```

**What happens**:
- Loads `nodejs.pdf`
- Splits into chunks
- Generates embeddings
- Stores in Qdrant

---

### **Step 4: Query the System**

```bash
# Run chat interface
python chat.py

# Prompt appears:
# Ask Something ... 

# Example query:
# What is the event loop in Node.js?

# Response:
# 🤖 Bot: The event loop in Node.js is a mechanism that...
#         For more details, see page 15 of the document.
```

---

## Best Practices

### **1. Chunk Size Optimization**

```python
# For technical docs
chunk_size = 1000
chunk_overlap = 400

# For narrative text
chunk_size = 1500
chunk_overlap = 200

# For code snippets
chunk_size = 500
chunk_overlap = 100
```

---

### **2. Embedding Model Selection**

| Model | Dimensions | Use Case |
|-------|-----------|----------|
| text-embedding-3-small | 1536 | Fast, cost-effective |
| text-embedding-3-large | 3072 | Best quality (used here) |
| text-embedding-ada-002 | 1536 | Legacy, still good |

---

### **3. Retrieval Tuning**

```python
# Adjust number of retrieved chunks
search_results = vector_db.similarity_search(
    query=user_query,
    k=4  # Try 3-10 depending on use case
)

# Add similarity threshold
search_results = vector_db.similarity_search_with_score(
    query=user_query,
    k=4,
    score_threshold=0.7  # Only return if >70% similar
)
```

---

### **4. Prompt Optimization**

**Good prompt**:
```python
SYSTEM_PROMPT = """
You are an expert on Node.js. Answer questions using ONLY the provided context.
If the context doesn't contain the answer, say "I don't have that information."
Always cite the page number.

Context: {context}
"""
```

**Bad prompt**:
```python
SYSTEM_PROMPT = """
Answer the question.
{context}
"""
```

---

### **5. Monitoring & Logging**

```python
# Add logging
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Log retrieval
logger.info(f"Retrieved {len(search_results)} chunks")
logger.info(f"Top chunk similarity: {search_results[0].score}")

# Log generation
logger.info(f"Generated answer: {response.choices[0].message.content[:100]}...")
```

---

### **6. Cost Optimization**

**Embedding costs**:
- text-embedding-3-large: $0.13 / 1M tokens
- For 100-page PDF (~50k words): ~$0.01

**LLM costs**:
- GPT-4o: $2.50 / 1M input tokens, $10 / 1M output tokens
- Average query: ~$0.01-0.02

**Tips**:
- Cache embeddings (don't re-index unnecessarily)
- Use smaller models for simple queries
- Implement rate limiting

---

### **7. Security**

```python
# ✅ DO: Use environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# ❌ DON'T: Hardcode keys
api_key = "sk-proj-..."

# ✅ DO: Add .env to .gitignore
# ❌ DON'T: Commit API keys to Git
```

---

## Advanced Concepts

### **Hybrid Search**

Combine vector search with keyword search:

```python
# Vector search
vector_results = vector_db.similarity_search(query)

# Keyword search (BM25)
keyword_results = bm25_search(query, documents)

# Combine results
final_results = merge_and_rerank(vector_results, keyword_results)
```

---

### **Re-ranking**

Improve retrieval quality:

```python
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import CohereRerank

# Add re-ranker
compressor = CohereRerank()
compression_retriever = ContextualCompressionRetriever(
    base_compressor=compressor,
    base_retriever=vector_db.as_retriever()
)
```

---

### **Multi-document RAG**

Index multiple PDFs:

```python
# Index multiple documents
pdf_files = ["nodejs.pdf", "python.pdf", "react.pdf"]

for pdf_file in pdf_files:
    loader = PyPDFLoader(pdf_file)
    docs = loader.load()
    chunks = text_splitter.split_documents(docs)
    
    # Add to same collection
    vector_store.add_documents(chunks)
```

---

### **Metadata Filtering**

Filter by document properties:

```python
# Search only in specific pages
results = vector_db.similarity_search(
    query=user_query,
    filter={"page_label": {"$gte": 10, "$lte": 20}}
)

# Search only in specific document
results = vector_db.similarity_search(
    query=user_query,
    filter={"source": "nodejs.pdf"}
)
```

---

## Troubleshooting

### **Issue 1: Qdrant Connection Error**

```
Error: Connection refused at localhost:6333
```

**Solution**:
```bash
# Check if Qdrant is running
docker ps | grep qdrant

# If not running, start it
docker-compose up -d

# Check logs
docker logs <container_id>
```

---

### **Issue 2: OpenAI API Error**

```
Error: Incorrect API key provided
```

**Solution**:
```bash
# Verify .env file
cat .env | grep OPENAI_API_KEY

# Test API key
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY"
```

---

### **Issue 3: No Results Found**

```
Retrieved 0 chunks
```

**Solution**:
```python
# Check if collection exists
from qdrant_client import QdrantClient

client = QdrantClient(url="http://localhost:6333")
collections = client.get_collections()
print(collections)

# Re-run indexing if needed
python index.py
```

---

### **Issue 4: Poor Answer Quality**

**Possible causes**:
1. Irrelevant chunks retrieved
2. Chunk size too small/large
3. Poor prompt design

**Solutions**:
```python
# 1. Increase k (retrieve more chunks)
search_results = vector_db.similarity_search(query=user_query, k=10)

# 2. Adjust chunk size
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1500,  # Increase
    chunk_overlap=500
)

# 3. Improve prompt
SYSTEM_PROMPT = """
You are an expert assistant. Provide detailed, accurate answers.
Use ONLY the context below. Cite page numbers.

Context: {context}
"""
```

---

## Performance Metrics

### **Indexing Performance**

| Document Size | Pages | Chunks | Time | Cost |
|--------------|-------|--------|------|------|
| Small (1MB) | 10 | 30 | 5s | $0.001 |
| Medium (5MB) | 50 | 150 | 20s | $0.005 |
| Large (20MB) | 200 | 600 | 80s | $0.02 |

---

### **Query Performance**

| Operation | Time | Cost |
|-----------|------|------|
| Embedding query | 100ms | $0.0001 |
| Vector search | 50ms | Free |
| LLM generation | 2s | $0.01 |
| **Total** | **~2.2s** | **~$0.01** |

---

## Conclusion

This RAG system provides:
- ✅ Fast, accurate document querying
- ✅ Scalable architecture
- ✅ Cost-effective solution
- ✅ Easy to extend and customize

**Next steps**:
1. Add more documents
2. Implement chat history
3. Add web interface
4. Deploy to production

---

## References

- [LangChain Documentation](https://python.langchain.com/)
- [Qdrant Documentation](https://qdrant.tech/documentation/)
- [OpenAI Embeddings Guide](https://platform.openai.com/docs/guides/embeddings)
- [RAG Paper (Lewis et al., 2020)](https://arxiv.org/abs/2005.11401)

---

**Last Updated**: January 2026  
**Version**: 1.0  
**Author**: Agentic AI Course
