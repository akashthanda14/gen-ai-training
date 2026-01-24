# RAG System - Quick Reference Notes

## 🎯 What is RAG?

**Retrieval-Augmented Generation** = Retrieval + LLM Generation

Instead of relying solely on the LLM's training data, RAG:
1. **Retrieves** relevant information from a knowledge base
2. **Augments** the prompt with this information
3. **Generates** an answer based on retrieved context

---

## 🏗️ System Components

### 1. **Vector Database (Qdrant)**
- Stores document embeddings
- Enables fast similarity search
- Runs on Docker at `localhost:6333`

### 2. **Embedding Model (OpenAI)**
- Model: `text-embedding-3-large`
- Converts text → 3072-dimensional vectors
- Same model used for both indexing and querying

### 3. **LLM (GPT-4o)**
- Generates final answers
- Uses retrieved context
- Cites page numbers

### 4. **LangChain Framework**
- Orchestrates the RAG pipeline
- Provides document loaders, splitters, vector stores
- Simplifies integration

---

## 📊 Two-Phase Process

### **Phase 1: Indexing** (One-time)
```
PDF → Extract Text → Split Chunks → Generate Embeddings → Store in Qdrant
```

### **Phase 2: Querying** (Every question)
```
Query → Embed Query → Search Vectors → Retrieve Chunks → Generate Answer
```

---

## 🔑 Key Concepts

### **Embeddings**
- Numerical representation of text
- Captures semantic meaning
- Similar texts have similar vectors

**Example**:
```
"Node.js is fast"  → [0.8, 0.9, 0.1, ...]
"Node.js is quick" → [0.79, 0.88, 0.12, ...]  ← Similar!
"Python is slow"   → [-0.5, -0.3, 0.7, ...]   ← Different!
```

---

### **Chunking**
- Breaking documents into smaller pieces
- **chunk_size**: 1000 characters
- **chunk_overlap**: 400 characters (prevents context loss)

**Why?**
- LLMs have token limits
- Smaller chunks = more precise retrieval
- Overlap maintains context at boundaries

---

### **Similarity Search**
- Finds chunks most similar to query
- Uses **cosine similarity**
- Returns top-k results (default: 4)

**Formula**:
```
similarity = cos(θ) = (A · B) / (||A|| × ||B||)
Range: -1 to 1 (1 = identical, 0 = unrelated)
```

---

## 📝 Code Walkthrough

### **index.py** (Indexing)

```python
# 1. Load PDF
loader = PyPDFLoader("nodejs.pdf")
docs = loader.load()

# 2. Split into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=400
)
chunks = text_splitter.split_documents(docs)

# 3. Create embeddings & store
embedding_model = OpenAIEmbeddings(model="text-embedding-3-large")
vector_store = QdrantVectorStore.from_documents(
    documents=chunks,
    embedding=embedding_model,
    url="http://localhost:6333",
    collection_name="learning-rag"
)
```

---

### **chat.py** (Querying)

```python
# 1. Connect to vector DB
embedding_model = OpenAIEmbeddings(model="text-embedding-3-large")
vector_db = QdrantVectorStore.from_existing_collection(
    url="http://localhost:6333",
    collection_name="learning-rag",
    embedding=embedding_model
)

# 2. Get user query
user_query = input("Ask Something ... ")

# 3. Retrieve relevant chunks
search_results = vector_db.similarity_search(query=user_query)

# 4. Format context
context = "\n\n\n".join([
    f"Page Content: {result.page_content}\n"
    f"Page Number: {result.metadata['page_label']}\n"
    f"File Location: {result.metadata['source']}"
    for result in search_results
])

# 5. Generate answer
response = openai_client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT.format(context=context)},
        {"role": "user", "content": user_query}
    ]
)
```

---

## 🚀 Quick Start

### **1. Start Qdrant**
```bash
cd /Users/work/Desktop/LLM/GEN-AI/prompts/rag
docker-compose up -d
```

### **2. Index Documents**
```bash
python index.py
```

### **3. Query**
```bash
python chat.py
```

---

## 💡 Important Notes

### **Embedding Model Consistency**
⚠️ **MUST use the same embedding model for indexing and querying**
- Indexing: `text-embedding-3-large`
- Querying: `text-embedding-3-large` ✅

Using different models will break similarity search!

---

### **Chunk Size Trade-offs**

| Chunk Size | Pros | Cons |
|-----------|------|------|
| Small (500) | Precise retrieval | May lose context |
| Medium (1000) | ✅ Balanced | ✅ Good default |
| Large (2000) | Full context | May include irrelevant info |

---

### **Number of Retrieved Chunks**

| k value | Use Case |
|---------|----------|
| 1-2 | Simple, focused questions |
| 3-5 | ✅ Most questions (default) |
| 6-10 | Complex, multi-faceted questions |
| 10+ | Comprehensive analysis |

---

## 🎨 Prompt Engineering

### **System Prompt Template**
```python
SYSTEM_PROMPT = """
You are a helpful AI Assistant who answers user queries based on the available context
retrieved from a PDF file along with page contents and page numbers.

You should only answer the user based on the following context and navigate the user
to open the right page number to know more.

context:{context}
"""
```

### **Key Elements**
1. **Role**: Define AI's role
2. **Constraint**: "only answer based on context"
3. **Guidance**: "navigate to page number"
4. **Context**: Inject retrieved chunks

---

## 📈 Performance

### **Indexing**
- 100 pages ≈ 300 chunks
- Time: ~30 seconds
- Cost: ~$0.01

### **Querying**
- Embedding: ~100ms
- Search: ~50ms
- Generation: ~2s
- **Total**: ~2.2s per query
- **Cost**: ~$0.01 per query

---

## 🔧 Common Issues

### **1. Qdrant not running**
```bash
# Check status
docker ps | grep qdrant

# Start if needed
docker-compose up -d
```

### **2. No results found**
- Verify collection exists
- Re-run indexing: `python index.py`
- Check embedding model consistency

### **3. Poor answer quality**
- Increase k (retrieve more chunks)
- Adjust chunk size
- Improve system prompt
- Add similarity threshold

---

## 📚 Best Practices

### ✅ DO
- Use environment variables for API keys
- Keep chunk size between 500-1500
- Add 20-40% overlap
- Cite sources in answers
- Log retrieval metrics

### ❌ DON'T
- Hardcode API keys
- Use different embedding models
- Make chunks too small (<200) or too large (>3000)
- Skip overlap (causes context loss)
- Ignore metadata

---

## 🎓 Teaching Points

### **Concept 1: Why Vector Embeddings?**
Traditional search: Keyword matching ("event loop" must appear)
Vector search: Semantic matching (understands "event loop" ≈ "async mechanism")

### **Concept 2: Why Chunking?**
- Can't fit entire book in LLM context
- Only need relevant sections
- Smaller chunks = better precision

### **Concept 3: Why RAG vs Fine-tuning?**
| Approach | Update Frequency | Cost | Use Case |
|----------|-----------------|------|----------|
| Fine-tuning | Rare | High | Stable knowledge |
| RAG | Real-time | Low | ✅ Dynamic documents |

### **Concept 4: Retrieval Quality**
Good retrieval = Good answers
- 80% of RAG quality comes from retrieval
- 20% from generation
- Focus on optimizing search first!

---

## 🔬 Advanced Topics

### **Hybrid Search**
Combine vector + keyword search for best results

### **Re-ranking**
Re-order retrieved chunks by relevance

### **Multi-document RAG**
Index multiple PDFs in same collection

### **Metadata Filtering**
Search only specific pages/documents

### **Chat History**
Maintain conversation context

---

## 📊 Metrics to Track

### **Retrieval Metrics**
- Number of chunks retrieved
- Average similarity score
- Retrieval time

### **Generation Metrics**
- Response time
- Token usage
- Cost per query

### **Quality Metrics**
- Answer relevance
- Citation accuracy
- User satisfaction

---

## 🛠️ Optimization Tips

### **1. Chunk Size**
```python
# Technical docs
chunk_size=1000, chunk_overlap=400

# Narrative text
chunk_size=1500, chunk_overlap=200

# Code
chunk_size=500, chunk_overlap=100
```

### **2. Retrieval**
```python
# Add similarity threshold
search_results = vector_db.similarity_search_with_score(
    query=user_query,
    k=5,
    score_threshold=0.7  # Only >70% similar
)
```

### **3. Cost Reduction**
- Cache embeddings (don't re-index)
- Use smaller models for simple queries
- Batch API calls
- Implement rate limiting

---

## 🔐 Security

```python
# ✅ Good
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# ❌ Bad
api_key = "sk-proj-..."

# ✅ Add to .gitignore
.env
```

---

## 📖 Further Reading

1. **RAG Paper**: [Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://arxiv.org/abs/2005.11401)
2. **LangChain Docs**: https://python.langchain.com/
3. **Qdrant Docs**: https://qdrant.tech/documentation/
4. **OpenAI Embeddings**: https://platform.openai.com/docs/guides/embeddings

---

## 🎯 Summary

**RAG in 3 Steps**:
1. **Index**: PDF → Chunks → Embeddings → Vector DB
2. **Retrieve**: Query → Search → Get relevant chunks
3. **Generate**: Context + Query → LLM → Answer

**Key Insight**: RAG grounds LLM responses in actual documents, reducing hallucinations and enabling up-to-date information retrieval.

---

**Version**: 1.0  
**Last Updated**: January 2026
