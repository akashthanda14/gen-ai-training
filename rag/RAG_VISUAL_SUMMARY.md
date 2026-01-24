# RAG System - Visual Summary

## 🎨 Complete System Visualization

```
╔═══════════════════════════════════════════════════════════════════════╗
║                    RAG SYSTEM - COMPLETE OVERVIEW                      ║
╚═══════════════════════════════════════════════════════════════════════╝

┌───────────────────────────────────────────────────────────────────────┐
│                         SYSTEM COMPONENTS                              │
└───────────────────────────────────────────────────────────────────────┘

    ┌─────────────────────────────────────────────────────────┐
    │                    INPUT LAYER                          │
    │                                                         │
    │  📄 nodejs.pdf (357KB, 42 pages)                       │
    │  ├─ Technical documentation                            │
    │  ├─ Text-based PDF                                     │
    │  └─ Source of knowledge                                │
    └────────────────────┬────────────────────────────────────┘
                         │
                         ▼
    ┌─────────────────────────────────────────────────────────┐
    │                  PROCESSING LAYER                       │
    │                                                         │
    │  🔧 index.py (Indexing Script)                         │
    │  ├─ PyPDFLoader: Extract text                         │
    │  ├─ TextSplitter: Create chunks (1000 chars)          │
    │  ├─ OpenAI API: Generate embeddings (3072-dim)        │
    │  └─ Result: 127 chunks indexed                        │
    └────────────────────┬────────────────────────────────────┘
                         │
                         ▼
    ┌─────────────────────────────────────────────────────────┐
    │                   STORAGE LAYER                         │
    │                                                         │
    │  🗄️ Qdrant Vector Database                             │
    │  ├─ Running on: localhost:6333                         │
    │  ├─ Collection: "learning-rag"                         │
    │  ├─ Vectors: 127 points (3072 dimensions each)        │
    │  └─ Metadata: page_content, page_label, source        │
    └────────────────────┬────────────────────────────────────┘
                         │
                         ▼
    ┌─────────────────────────────────────────────────────────┐
    │                   QUERY LAYER                           │
    │                                                         │
    │  💬 chat.py (Query Interface)                          │
    │  ├─ User Input: Question                               │
    │  ├─ Embedding: Convert to vector                       │
    │  ├─ Search: Find top 4 similar chunks                  │
    │  └─ Generate: GPT-4o creates answer                    │
    └────────────────────┬────────────────────────────────────┘
                         │
                         ▼
    ┌─────────────────────────────────────────────────────────┐
    │                   OUTPUT LAYER                          │
    │                                                         │
    │  🤖 AI Response                                         │
    │  ├─ Answer based on retrieved context                  │
    │  ├─ Page number citations                              │
    │  └─ Grounded in actual document content                │
    └─────────────────────────────────────────────────────────┘


┌───────────────────────────────────────────────────────────────────────┐
│                         DATA FLOW                                      │
└───────────────────────────────────────────────────────────────────────┘

INDEXING PHASE (One-time setup):

📄 PDF File
    │
    ├─→ [Extract] → 📝 Raw Text (42 pages)
    │
    ├─→ [Split] → 📋 Text Chunks (127 chunks)
    │                  ├─ Chunk 1: "Node.js is a JavaScript..."
    │                  ├─ Chunk 2: "...runtime built on Chrome's..."
    │                  └─ Chunk 3: "...V8 engine. The event loop..."
    │
    ├─→ [Embed] → 🔢 Vectors (127 × 3072 dimensions)
    │                  ├─ Vector 1: [0.234, -0.891, 0.456, ...]
    │                  ├─ Vector 2: [0.123, 0.567, -0.234, ...]
    │                  └─ Vector 3: [-0.456, 0.789, 0.123, ...]
    │
    └─→ [Store] → 🗄️ Qdrant Database
                       └─ Collection: "learning-rag" ✅


QUERY PHASE (Every question):

👤 User Question: "What is the event loop?"
    │
    ├─→ [Embed] → 🔢 Query Vector: [0.345, -0.678, 0.912, ...]
    │
    ├─→ [Search] → 🔍 Similarity Calculation
    │                  ├─ Compare with all 127 vectors
    │                  ├─ Calculate cosine similarity
    │                  └─ Rank by similarity score
    │
    ├─→ [Retrieve] → 📋 Top 4 Chunks
    │                    ├─ Chunk 45 (Score: 0.92) - Page 15
    │                    ├─ Chunk 78 (Score: 0.89) - Page 16
    │                    ├─ Chunk 12 (Score: 0.85) - Page 15
    │                    └─ Chunk 91 (Score: 0.82) - Page 17
    │
    ├─→ [Format] → 📝 Context String
    │                  "Page Content: The event loop is...
    │                   Page Number: 15
    │                   File Location: nodejs.pdf"
    │
    ├─→ [Generate] → 🤖 GPT-4o Processing
    │                    ├─ System: Instructions
    │                    ├─ Context: Retrieved chunks
    │                    └─ User: Original question
    │
    └─→ [Display] → 💬 Final Answer
                        "The event loop in Node.js is a mechanism
                         that handles asynchronous operations.
                         For more details, see page 15."


┌───────────────────────────────────────────────────────────────────────┐
│                    TECHNOLOGY STACK                                    │
└───────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  LAYER 1: Document Processing                              │
├─────────────────────────────────────────────────────────────┤
│  • PyPDFLoader (LangChain)                                 │
│  • RecursiveCharacterTextSplitter (LangChain)             │
└─────────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│  LAYER 2: Embeddings                                       │
├─────────────────────────────────────────────────────────────┤
│  • OpenAI Embeddings API                                   │
│  • Model: text-embedding-3-large                           │
│  • Dimensions: 3072                                        │
└─────────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│  LAYER 3: Vector Storage                                   │
├─────────────────────────────────────────────────────────────┤
│  • Qdrant Vector Database                                  │
│  • Docker Container                                        │
│  • Port: 6333                                              │
└─────────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│  LAYER 4: Retrieval                                        │
├─────────────────────────────────────────────────────────────┤
│  • QdrantVectorStore (LangChain)                          │
│  • Similarity Search (Cosine)                             │
│  • Top-k Retrieval (k=4)                                  │
└─────────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│  LAYER 5: Generation                                       │
├─────────────────────────────────────────────────────────────┤
│  • OpenAI GPT-4o                                           │
│  • Chat Completions API                                    │
│  • Context-aware generation                                │
└─────────────────────────────────────────────────────────────┘


┌───────────────────────────────────────────────────────────────────────┐
│                    PERFORMANCE METRICS                                 │
└───────────────────────────────────────────────────────────────────────┘

INDEXING (One-time):
┌──────────────────────┬──────────┬──────────┬──────────┐
│ Operation            │ Time     │ Cost     │ Output   │
├──────────────────────┼──────────┼──────────┼──────────┤
│ PDF Loading          │ 2s       │ Free     │ 42 pages │
│ Text Splitting       │ 1s       │ Free     │ 127 chunks│
│ Embedding Generation │ 25s      │ $0.01    │ 127 vectors│
│ Vector Storage       │ 2s       │ Free     │ 1 collection│
├──────────────────────┼──────────┼──────────┼──────────┤
│ TOTAL                │ ~30s     │ ~$0.01   │ ✅ Ready │
└──────────────────────┴──────────┴──────────┴──────────┘

QUERYING (Per question):
┌──────────────────────┬──────────┬──────────┬──────────┐
│ Operation            │ Time     │ Cost     │ Output   │
├──────────────────────┼──────────┼──────────┼──────────┤
│ Query Embedding      │ 100ms    │ $0.0001  │ 1 vector │
│ Similarity Search    │ 50ms     │ Free     │ 4 chunks │
│ Context Formatting   │ 10ms     │ Free     │ 1 prompt │
│ GPT-4o Generation    │ 2s       │ $0.01    │ 1 answer │
├──────────────────────┼──────────┼──────────┼──────────┤
│ TOTAL                │ ~2.2s    │ ~$0.01   │ ✅ Answer│
└──────────────────────┴──────────┴──────────┴──────────┘


┌───────────────────────────────────────────────────────────────────────┐
│                    CONFIGURATION PARAMETERS                            │
└───────────────────────────────────────────────────────────────────────┘

CHUNKING STRATEGY:
┌─────────────────────────────────────────────────────────┐
│  chunk_size = 1000 characters                          │
│  ├─ Too small (< 500): Loss of context                │
│  ├─ Optimal (500-1500): Balanced ✅                    │
│  └─ Too large (> 2000): Irrelevant info included      │
│                                                         │
│  chunk_overlap = 400 characters (40%)                  │
│  ├─ Prevents context loss at boundaries               │
│  ├─ Ensures complete sentences                        │
│  └─ Improves retrieval quality                        │
└─────────────────────────────────────────────────────────┘

EMBEDDING MODEL:
┌─────────────────────────────────────────────────────────┐
│  text-embedding-3-large                                │
│  ├─ Dimensions: 3072                                   │
│  ├─ Cost: $0.13 / 1M tokens                           │
│  ├─ Quality: Best available ✅                         │
│  └─ Use case: High-quality semantic search            │
└─────────────────────────────────────────────────────────┘

RETRIEVAL SETTINGS:
┌─────────────────────────────────────────────────────────┐
│  top_k = 4 chunks                                      │
│  ├─ Simple questions: 1-2 chunks                      │
│  ├─ Most questions: 3-5 chunks ✅                      │
│  └─ Complex questions: 6-10 chunks                    │
│                                                         │
│  similarity_metric = cosine                            │
│  ├─ Range: -1 to 1                                    │
│  ├─ 1 = Identical                                     │
│  └─ 0 = Unrelated                                     │
└─────────────────────────────────────────────────────────┘

GENERATION MODEL:
┌─────────────────────────────────────────────────────────┐
│  gpt-4o                                                │
│  ├─ Input: $2.50 / 1M tokens                          │
│  ├─ Output: $10 / 1M tokens                           │
│  ├─ Speed: Fast ✅                                     │
│  └─ Quality: High reasoning ability                   │
└─────────────────────────────────────────────────────────┘


┌───────────────────────────────────────────────────────────────────────┐
│                    VECTOR SIMILARITY EXPLAINED                         │
└───────────────────────────────────────────────────────────────────────┘

CONCEPT: Similar texts have similar vectors

Example (simplified to 3D for visualization):

Text 1: "Node.js is fast"
Vector 1: [0.8, 0.9, 0.1]
         │
         │ Cosine Similarity = 0.99 (Very similar!)
         │
Text 2: "Node.js is quick"
Vector 2: [0.79, 0.88, 0.12]


Text 3: "Python is slow"
Vector 3: [-0.5, -0.3, 0.7]
         │
         │ Cosine Similarity = 0.12 (Not similar)
         │
Vector 1: [0.8, 0.9, 0.1]


VISUAL REPRESENTATION:

    Y
    │
    │  • Vec1 (Node.js is fast)
    │  • Vec2 (Node.js is quick)  ← Close together!
    │
    │
    │
    │                    • Vec3 (Python is slow)  ← Far away!
    │
    └────────────────────────────────────────── X


┌───────────────────────────────────────────────────────────────────────┐
│                    CHUNKING VISUALIZATION                              │
└───────────────────────────────────────────────────────────────────────┘

Original Document:
┌─────────────────────────────────────────────────────────────┐
│ Node.js is a JavaScript runtime built on Chrome's V8       │
│ engine. The event loop is a mechanism that handles         │
│ asynchronous operations in Node.js. It continuously        │
│ checks for tasks in the callback queue and executes        │
│ them when the call stack is empty.                         │
└─────────────────────────────────────────────────────────────┘

After Chunking (chunk_size=100, overlap=40):
┌─────────────────────────────────────────────────────────────┐
│ Chunk 1:                                                    │
│ "Node.js is a JavaScript runtime built on Chrome's V8      │
│  engine. The event loop is a..."                           │
│                                                             │
│ Chunk 2:                                                    │
│ "...The event loop is a mechanism that handles             │
│  asynchronous operations in Node.js. It..."                │
│                                                             │
│ Chunk 3:                                                    │
│ "...It continuously checks for tasks in the callback       │
│  queue and executes them when the call stack is empty."    │
└─────────────────────────────────────────────────────────────┘
         └──────┘
         Overlap region (maintains context)


┌───────────────────────────────────────────────────────────────────────┐
│                    PROMPT STRUCTURE                                    │
└───────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  SYSTEM MESSAGE                                             │
├─────────────────────────────────────────────────────────────┤
│  You are a helpful AI Assistant who answers user queries   │
│  based on the available context retrieved from a PDF file  │
│  along with page contents and page numbers.                │
│                                                             │
│  You should only answer the user based on the following    │
│  context and navigate the user to open the right page      │
│  number to know more.                                      │
│                                                             │
│  CONTEXT:                                                  │
│  ┌───────────────────────────────────────────────────┐    │
│  │ Page Content: The event loop is a mechanism...    │    │
│  │ Page Number: 15                                   │    │
│  │ File Location: nodejs.pdf                         │    │
│  │                                                   │    │
│  │ Page Content: ...handles async operations...     │    │
│  │ Page Number: 16                                   │    │
│  │ File Location: nodejs.pdf                         │    │
│  └───────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│  USER MESSAGE                                               │
├─────────────────────────────────────────────────────────────┤
│  What is the event loop in Node.js?                        │
└─────────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│  ASSISTANT RESPONSE                                         │
├─────────────────────────────────────────────────────────────┤
│  The event loop in Node.js is a mechanism that handles     │
│  asynchronous operations. It continuously checks for       │
│  tasks in the callback queue and executes them when the    │
│  call stack is empty. For more details, see page 15 of     │
│  the document.                                             │
└─────────────────────────────────────────────────────────────┘


┌───────────────────────────────────────────────────────────────────────┐
│                    FILE STRUCTURE                                      │
└───────────────────────────────────────────────────────────────────────┘

rag/
│
├── 📄 index.py (4.5 KB)
│   ├─ Purpose: Index PDF into vector database
│   ├─ Input: nodejs.pdf
│   ├─ Output: Qdrant collection "learning-rag"
│   └─ Run: python index.py
│
├── 💬 chat.py (4.9 KB)
│   ├─ Purpose: Query indexed documents
│   ├─ Input: User question
│   ├─ Output: AI-generated answer
│   └─ Run: python chat.py
│
├── 📚 nodejs.pdf (358 KB)
│   ├─ Purpose: Sample document
│   ├─ Pages: 42
│   └─ Type: Technical documentation
│
├── 🐳 docker-compose.yml (79 B)
│   ├─ Purpose: Qdrant configuration
│   ├─ Service: vector-db
│   └─ Port: 6333
│
├── 🔐 .env (234 B)
│   ├─ Purpose: API keys
│   ├─ OPENAI_API_KEY
│   └─ GEMINI_API_KEY
│
├── 📖 README.md (11.6 KB)
│   ├─ Purpose: Overview and quick start
│   └─ Audience: Beginners
│
├── 📋 RAG_NOTES.md (9.1 KB)
│   ├─ Purpose: Quick reference notes
│   └─ Audience: All levels
│
├── 🏗️ RAG_ARCHITECTURE.md (27.7 KB)
│   ├─ Purpose: Complete architecture guide
│   └─ Audience: Advanced learners
│
└── 🔄 RAG_FLOW_DIAGRAMS.md (33.7 KB)
    ├─ Purpose: Visual flow diagrams
    └─ Audience: Visual learners


┌───────────────────────────────────────────────────────────────────────┐
│                    QUICK REFERENCE                                     │
└───────────────────────────────────────────────────────────────────────┘

COMMANDS:
┌─────────────────────────────────────────────────────────────┐
│  # Start Qdrant                                             │
│  docker-compose up -d                                       │
│                                                             │
│  # Check Qdrant status                                     │
│  curl http://localhost:6333/health                         │
│                                                             │
│  # Index documents                                         │
│  python index.py                                           │
│                                                             │
│  # Query system                                            │
│  python chat.py                                            │
│                                                             │
│  # Stop Qdrant                                             │
│  docker-compose down                                       │
└─────────────────────────────────────────────────────────────┘

KEY CONCEPTS:
┌─────────────────────────────────────────────────────────────┐
│  • Embeddings: Text → Numerical vectors                    │
│  • Chunking: Large docs → Small pieces                     │
│  • Similarity: Find related chunks                         │
│  • Augmentation: Add context to prompt                     │
│  • Generation: LLM creates answer                          │
└─────────────────────────────────────────────────────────────┘

BEST PRACTICES:
┌─────────────────────────────────────────────────────────────┐
│  ✅ Use same embedding model for indexing & querying       │
│  ✅ Add 20-40% overlap between chunks                      │
│  ✅ Keep chunk size 500-1500 characters                    │
│  ✅ Retrieve 3-5 chunks for most questions                 │
│  ✅ Always cite page numbers in answers                    │
│  ✅ Use environment variables for API keys                 │
└─────────────────────────────────────────────────────────────┘
```

---

**Version**: 1.0  
**Last Updated**: January 2026  
**Purpose**: Visual reference for RAG system architecture and operation
