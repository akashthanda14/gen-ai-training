# RAG System - Flow Diagrams

## 📊 Complete System Flow

```
╔═══════════════════════════════════════════════════════════════════════╗
║                         RAG SYSTEM OVERVIEW                            ║
╚═══════════════════════════════════════════════════════════════════════╝

┌─────────────────────────────────────────────────────────────────────────┐
│                          PHASE 1: INDEXING                              │
│                         (Run Once: index.py)                            │
└─────────────────────────────────────────────────────────────────────────┘

    📄 nodejs.pdf
         │
         │ PyPDFLoader.load()
         ▼
    ┌─────────────────────────────────────┐
    │  Document Objects (Pages)           │
    │  ┌───────────────────────────────┐  │
    │  │ Page 1: "Node.js is a..."     │  │
    │  │ Page 2: "Event loop..."       │  │
    │  │ Page 3: "Modules..."          │  │
    │  └───────────────────────────────┘  │
    └─────────────┬───────────────────────┘
                  │
                  │ RecursiveCharacterTextSplitter
                  │ chunk_size=1000, overlap=400
                  ▼
    ┌─────────────────────────────────────┐
    │  Text Chunks                        │
    │  ┌───────────────────────────────┐  │
    │  │ Chunk 1: "Node.js is a..."    │  │
    │  │ Chunk 2: "...runtime built..."│  │
    │  │ Chunk 3: "...V8 engine..."    │  │
    │  │ ... (127 chunks total)        │  │
    │  └───────────────────────────────┘  │
    └─────────────┬───────────────────────┘
                  │
                  │ OpenAI Embeddings API
                  │ model: text-embedding-3-large
                  ▼
    ┌─────────────────────────────────────┐
    │  Vector Embeddings (3072-dim)       │
    │  ┌───────────────────────────────┐  │
    │  │ [0.234, -0.891, 0.456, ...]   │  │
    │  │ [0.123, 0.567, -0.234, ...]   │  │
    │  │ [-0.456, 0.789, 0.123, ...]   │  │
    │  └───────────────────────────────┘  │
    └─────────────┬───────────────────────┘
                  │
                  │ QdrantVectorStore.from_documents()
                  ▼
    ┌─────────────────────────────────────┐
    │  Qdrant Vector Database             │
    │  Collection: "learning-rag"         │
    │  URL: http://localhost:6333         │
    │  ┌───────────────────────────────┐  │
    │  │ Point 1:                      │  │
    │  │   Vector: [0.234, ...]        │  │
    │  │   Payload: {                  │  │
    │  │     page_content: "...",      │  │
    │  │     page_label: "1",          │  │
    │  │     source: "nodejs.pdf"      │  │
    │  │   }                           │  │
    │  │ Point 2: ...                  │  │
    │  │ Point 3: ...                  │  │
    │  └───────────────────────────────┘  │
    └─────────────────────────────────────┘
              ✅ Ready for Queries!


┌─────────────────────────────────────────────────────────────────────────┐
│                          PHASE 2: QUERYING                              │
│                    (Every Question: chat.py)                            │
└─────────────────────────────────────────────────────────────────────────┘

    👤 User Input
         │
         │ input("Ask Something ... ")
         ▼
    ┌─────────────────────────────────────┐
    │  User Query                         │
    │  "What is the event loop in         │
    │   Node.js?"                         │
    └─────────────┬───────────────────────┘
                  │
                  │ OpenAI Embeddings API
                  │ model: text-embedding-3-large
                  ▼
    ┌─────────────────────────────────────┐
    │  Query Vector (3072-dim)            │
    │  [0.345, -0.678, 0.912, ...]        │
    └─────────────┬───────────────────────┘
                  │
                  │ vector_db.similarity_search()
                  │ Cosine Similarity Calculation
                  ▼
    ┌─────────────────────────────────────┐
    │  Qdrant Vector Database             │
    │  ┌───────────────────────────────┐  │
    │  │ Calculate similarity with     │  │
    │  │ all 127 stored vectors        │  │
    │  │                               │  │
    │  │ Scores:                       │  │
    │  │ Point 45: 0.92 ← Most similar │  │
    │  │ Point 78: 0.89               │  │
    │  │ Point 12: 0.85               │  │
    │  │ Point 91: 0.82               │  │
    │  │ ...                          │  │
    │  └───────────────────────────────┘  │
    └─────────────┬───────────────────────┘
                  │
                  │ Return top 4 chunks
                  ▼
    ┌─────────────────────────────────────┐
    │  Retrieved Chunks                   │
    │  ┌───────────────────────────────┐  │
    │  │ Chunk 1 (Score: 0.92):        │  │
    │  │   Content: "The event loop    │  │
    │  │            is a mechanism..." │  │
    │  │   Page: 15                    │  │
    │  │   Source: nodejs.pdf          │  │
    │  │                               │  │
    │  │ Chunk 2 (Score: 0.89):        │  │
    │  │   Content: "...handles async" │  │
    │  │   Page: 16                    │  │
    │  │                               │  │
    │  │ Chunk 3, Chunk 4...           │  │
    │  └───────────────────────────────┘  │
    └─────────────┬───────────────────────┘
                  │
                  │ Format context string
                  ▼
    ┌─────────────────────────────────────┐
    │  Formatted Context                  │
    │  ┌───────────────────────────────┐  │
    │  │ Page Content: The event loop  │  │
    │  │ is a mechanism...             │  │
    │  │ Page Number: 15               │  │
    │  │ File Location: nodejs.pdf     │  │
    │  │                               │  │
    │  │ Page Content: ...handles      │  │
    │  │ async operations...           │  │
    │  │ Page Number: 16               │  │
    │  │ File Location: nodejs.pdf     │  │
    │  └───────────────────────────────┘  │
    └─────────────┬───────────────────────┘
                  │
                  │ Build prompt
                  ▼
    ┌─────────────────────────────────────┐
    │  Complete Prompt                    │
    │  ┌───────────────────────────────┐  │
    │  │ System: "You are a helpful    │  │
    │  │         AI Assistant..."      │  │
    │  │                               │  │
    │  │ Context: [Retrieved chunks]   │  │
    │  │                               │  │
    │  │ User: "What is the event loop │  │
    │  │        in Node.js?"           │  │
    │  └───────────────────────────────┘  │
    └─────────────┬───────────────────────┘
                  │
                  │ openai_client.chat.completions.create()
                  │ model: gpt-4o
                  ▼
    ┌─────────────────────────────────────┐
    │  GPT-4o Processing                  │
    │  ┌───────────────────────────────┐  │
    │  │ 1. Read system instructions   │  │
    │  │ 2. Analyze context            │  │
    │  │ 3. Understand user query      │  │
    │  │ 4. Generate answer            │  │
    │  │ 5. Cite page numbers          │  │
    │  └───────────────────────────────┘  │
    └─────────────┬───────────────────────┘
                  │
                  │ response.choices[0].message.content
                  ▼
    ┌─────────────────────────────────────┐
    │  Final Answer                       │
    │  ┌───────────────────────────────┐  │
    │  │ 🤖 Bot: The event loop in     │  │
    │  │ Node.js is a mechanism that   │  │
    │  │ handles asynchronous          │  │
    │  │ operations. It continuously   │  │
    │  │ checks for tasks in the       │  │
    │  │ callback queue and executes   │  │
    │  │ them when the call stack is   │  │
    │  │ empty. For more details, see  │  │
    │  │ page 15 of the document.      │  │
    │  └───────────────────────────────┘  │
    └─────────────────────────────────────┘
              👤 Displayed to User
```

---

## 🔄 Detailed Process Flow

### **1. Indexing Flow (Step-by-Step)**

```
START
  │
  ├─→ [1] Load Environment Variables
  │     │
  │     └─→ load_dotenv()
  │           │
  │           └─→ OPENAI_API_KEY loaded
  │
  ├─→ [2] Initialize PDF Loader
  │     │
  │     └─→ PyPDFLoader(file_path="nodejs.pdf")
  │
  ├─→ [3] Load PDF Document
  │     │
  │     └─→ loader.load()
  │           │
  │           ├─→ Extract page 1 → Document object
  │           ├─→ Extract page 2 → Document object
  │           ├─→ Extract page 3 → Document object
  │           └─→ ... (all pages)
  │                 │
  │                 └─→ List of Document objects
  │
  ├─→ [4] Initialize Text Splitter
  │     │
  │     └─→ RecursiveCharacterTextSplitter(
  │           chunk_size=1000,
  │           chunk_overlap=400
  │         )
  │
  ├─→ [5] Split Documents into Chunks
  │     │
  │     └─→ text_splitter.split_documents(docs)
  │           │
  │           ├─→ For each document:
  │           │     │
  │           │     ├─→ Split into 1000-char chunks
  │           │     ├─→ Add 400-char overlap
  │           │     └─→ Preserve metadata
  │           │
  │           └─→ List of chunk Document objects
  │
  ├─→ [6] Initialize Embedding Model
  │     │
  │     └─→ OpenAIEmbeddings(
  │           model="text-embedding-3-large"
  │         )
  │
  ├─→ [7] Create Vector Store
  │     │
  │     └─→ QdrantVectorStore.from_documents()
  │           │
  │           ├─→ For each chunk:
  │           │     │
  │           │     ├─→ Call OpenAI API
  │           │     │     │
  │           │     │     └─→ Get 3072-dim vector
  │           │     │
  │           │     └─→ Store in Qdrant:
  │           │           │
  │           │           ├─→ Vector: [0.234, ...]
  │           │           └─→ Payload: {
  │           │                 page_content: "...",
  │           │                 page_label: "1",
  │           │                 source: "nodejs.pdf"
  │           │               }
  │           │
  │           └─→ Collection "learning-rag" created
  │
  └─→ [8] Print Success Message
        │
        └─→ "✅ Indexing of Documents done..."
              │
              └─→ END
```

---

### **2. Query Flow (Step-by-Step)**

```
START
  │
  ├─→ [1] Load Environment Variables
  │     │
  │     └─→ load_dotenv()
  │
  ├─→ [2] Initialize OpenAI Client
  │     │
  │     └─→ OpenAI()
  │
  ├─→ [3] Initialize Embedding Model
  │     │
  │     └─→ OpenAIEmbeddings(
  │           model="text-embedding-3-large"
  │         )
  │
  ├─→ [4] Connect to Existing Vector DB
  │     │
  │     └─→ QdrantVectorStore.from_existing_collection(
  │           url="http://localhost:6333",
  │           collection_name="learning-rag",
  │           embedding=embedding_model
  │         )
  │
  ├─→ [5] Get User Input
  │     │
  │     └─→ input("Ask Something ... ")
  │           │
  │           └─→ user_query = "What is the event loop?"
  │
  ├─→ [6] Perform Similarity Search
  │     │
  │     └─→ vector_db.similarity_search(user_query)
  │           │
  │           ├─→ Embed user query
  │           │     │
  │           │     └─→ OpenAI API call
  │           │           │
  │           │           └─→ Query vector: [0.345, ...]
  │           │
  │           ├─→ Calculate similarity with all vectors
  │           │     │
  │           │     ├─→ For each stored vector:
  │           │     │     │
  │           │     │     └─→ cosine_similarity(query_vec, stored_vec)
  │           │     │
  │           │     └─→ Sort by similarity score
  │           │
  │           └─→ Return top 4 chunks
  │                 │
  │                 └─→ [chunk1, chunk2, chunk3, chunk4]
  │
  ├─→ [7] Format Context
  │     │
  │     └─→ For each search result:
  │           │
  │           ├─→ Extract page_content
  │           ├─→ Extract page_label
  │           ├─→ Extract source
  │           │
  │           └─→ Format as string:
  │                 "Page Content: ...\n
  │                  Page Number: ...\n
  │                  File Location: ..."
  │
  ├─→ [8] Build System Prompt
  │     │
  │     └─→ SYSTEM_PROMPT_TEMPLATE.format(context=context)
  │           │
  │           └─→ Complete system prompt with context
  │
  ├─→ [9] Call GPT-4o
  │     │
  │     └─→ openai_client.chat.completions.create(
  │           model="gpt-4o",
  │           messages=[
  │             {"role": "system", "content": final_system_prompt},
  │             {"role": "user", "content": user_query}
  │           ]
  │         )
  │           │
  │           ├─→ GPT-4o processes:
  │           │     │
  │           │     ├─→ Read system instructions
  │           │     ├─→ Analyze context
  │           │     ├─→ Understand query
  │           │     └─→ Generate answer
  │           │
  │           └─→ Response object
  │
  └─→ [10] Display Answer
        │
        └─→ print(response.choices[0].message.content)
              │
              └─→ END
```

---

## 🎯 Data Transformation Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    DATA TRANSFORMATION                          │
└─────────────────────────────────────────────────────────────────┘

INDEXING PHASE:

PDF File (Binary)
    │
    ▼
Raw Text (String)
    "Node.js is a JavaScript runtime built on Chrome's V8 engine..."
    │
    ▼
Document Objects (List)
    [
      Document(page_content="Node.js is...", metadata={page: 0}),
      Document(page_content="Event loop...", metadata={page: 1})
    ]
    │
    ▼
Text Chunks (List)
    [
      Document(page_content="Node.js is a JavaScript...", metadata={...}),
      Document(page_content="...runtime built on Chrome's...", metadata={...}),
      Document(page_content="...V8 engine. The event loop...", metadata={...})
    ]
    │
    ▼
Vector Embeddings (List of Arrays)
    [
      [0.234, -0.891, 0.456, ..., 0.123],  # 3072 dimensions
      [0.123, 0.567, -0.234, ..., 0.456],
      [-0.456, 0.789, 0.123, ..., 0.789]
    ]
    │
    ▼
Qdrant Points (Stored in Database)
    {
      id: 1,
      vector: [0.234, -0.891, ...],
      payload: {
        page_content: "Node.js is a JavaScript...",
        page_label: "1",
        source: "nodejs.pdf"
      }
    }


QUERY PHASE:

User Query (String)
    "What is the event loop in Node.js?"
    │
    ▼
Query Vector (Array)
    [0.345, -0.678, 0.912, ..., 0.234]  # 3072 dimensions
    │
    ▼
Similarity Scores (List of Tuples)
    [
      (Point 45, 0.92),
      (Point 78, 0.89),
      (Point 12, 0.85),
      (Point 91, 0.82)
    ]
    │
    ▼
Retrieved Documents (List)
    [
      Document(page_content="The event loop is...", metadata={page: 15}),
      Document(page_content="...handles async...", metadata={page: 16}),
      Document(page_content="...callback queue...", metadata={page: 15}),
      Document(page_content="...call stack...", metadata={page: 17})
    ]
    │
    ▼
Formatted Context (String)
    "Page Content: The event loop is a mechanism...
     Page Number: 15
     File Location: nodejs.pdf
     
     Page Content: ...handles async operations...
     Page Number: 16
     File Location: nodejs.pdf"
    │
    ▼
Complete Prompt (Dict)
    {
      "messages": [
        {
          "role": "system",
          "content": "You are a helpful AI...\ncontext: [context]"
        },
        {
          "role": "user",
          "content": "What is the event loop in Node.js?"
        }
      ]
    }
    │
    ▼
LLM Response (Object)
    ChatCompletion(
      choices=[
        Choice(
          message=Message(
            content="The event loop in Node.js is..."
          )
        )
      ]
    )
    │
    ▼
Final Answer (String)
    "The event loop in Node.js is a mechanism that handles
     asynchronous operations. For more details, see page 15."
```

---

## 🔀 Decision Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    DECISION POINTS                              │
└─────────────────────────────────────────────────────────────────┘

User runs: python index.py
    │
    ├─→ Does .env exist?
    │     ├─→ NO → ERROR: "OPENAI_API_KEY not found"
    │     └─→ YES → Continue
    │
    ├─→ Does nodejs.pdf exist?
    │     ├─→ NO → ERROR: "File not found"
    │     └─→ YES → Continue
    │
    ├─→ Is Qdrant running?
    │     ├─→ NO → ERROR: "Connection refused"
    │     └─→ YES → Continue
    │
    ├─→ Can extract text from PDF?
    │     ├─→ NO → ERROR: "PDF is image-based or corrupted"
    │     └─→ YES → Continue
    │
    ├─→ Are chunks created?
    │     ├─→ NO → WARNING: "No chunks created"
    │     └─→ YES → Continue
    │
    ├─→ OpenAI API call successful?
    │     ├─→ NO → ERROR: "API error"
    │     └─→ YES → Continue
    │
    └─→ Qdrant storage successful?
          ├─→ NO → ERROR: "Storage failed"
          └─→ YES → ✅ SUCCESS


User runs: python chat.py
    │
    ├─→ Does .env exist?
    │     ├─→ NO → ERROR: "OPENAI_API_KEY not found"
    │     └─→ YES → Continue
    │
    ├─→ Is Qdrant running?
    │     ├─→ NO → ERROR: "Connection refused"
    │     └─→ YES → Continue
    │
    ├─→ Does collection exist?
    │     ├─→ NO → ERROR: "Collection not found. Run index.py first"
    │     └─→ YES → Continue
    │
    ├─→ User enters query
    │     │
    │     └─→ Is query empty?
    │           ├─→ YES → Prompt again
    │           └─→ NO → Continue
    │
    ├─→ Embedding successful?
    │     ├─→ NO → ERROR: "API error"
    │     └─→ YES → Continue
    │
    ├─→ Search returns results?
    │     ├─→ NO → "No relevant information found"
    │     └─→ YES → Continue
    │
    ├─→ GPT-4o call successful?
    │     ├─→ NO → ERROR: "Generation failed"
    │     └─→ YES → Continue
    │
    └─→ Display answer
          │
          └─→ ✅ SUCCESS
```

---

## 🌊 Parallel vs Sequential Operations

```
┌─────────────────────────────────────────────────────────────────┐
│                    OPERATION TIMELINE                           │
└─────────────────────────────────────────────────────────────────┘

INDEXING (Sequential - must happen in order):

Time →
0s    ├─ Load PDF ────────────┤
2s                             ├─ Split Chunks ─┤
3s                                               ├─ Embed Chunk 1 ──┤
4s                                               ├─ Embed Chunk 2 ──┤
5s                                               ├─ Embed Chunk 3 ──┤
...                                              ...
30s                                                                  ├─ Store ─┤
31s                                                                           ✅


QUERYING (Mostly sequential, some parallel):

Time →
0s    ├─ Get User Input ─────┤
1s                            ├─ Embed Query ──┤
1.1s                                           ├─ Search DB ─┤
1.15s                                                        ├─ Format Context ─┤
1.2s                                                                           ├─ GPT-4o ────────┤
3.2s                                                                                            ✅


BATCH INDEXING (Can parallelize embeddings):

Sequential:
  Chunk 1 → Embed → Chunk 2 → Embed → Chunk 3 → Embed
  Total: 30s for 100 chunks

Parallel (10 at a time):
  Chunk 1-10 → Embed (parallel)
  Chunk 11-20 → Embed (parallel)
  ...
  Total: 3s for 100 chunks (10x faster!)
```

---

## 📊 Component Interaction Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                    COMPONENT INTERACTIONS                       │
└─────────────────────────────────────────────────────────────────┘

┌──────────────┐
│   index.py   │
└──────┬───────┘
       │
       ├─────────────────────┐
       │                     │
       ▼                     ▼
┌──────────────┐      ┌──────────────┐
│ PyPDFLoader  │      │  pathlib     │
└──────┬───────┘      └──────────────┘
       │
       ▼
┌─────────────────────────────────┐
│ RecursiveCharacterTextSplitter  │
└──────┬──────────────────────────┘
       │
       ▼
┌──────────────────┐
│ OpenAIEmbeddings │◄──────────┐
└──────┬───────────┘           │
       │                       │
       ▼                       │
┌──────────────────┐           │
│ QdrantVectorStore│           │
└──────┬───────────┘           │
       │                       │
       ▼                       │
┌──────────────────┐           │
│  Qdrant Server   │           │
│  (Docker)        │           │
└──────────────────┘           │
                               │
                               │
┌──────────────┐               │
│   chat.py    │               │
└──────┬───────┘               │
       │                       │
       ├───────────────────────┘
       │
       ├─────────────────────┐
       │                     │
       ▼                     ▼
┌──────────────────┐   ┌──────────────┐
│ QdrantVectorStore│   │ OpenAI Client│
└──────┬───────────┘   └──────┬───────┘
       │                      │
       ▼                      │
┌──────────────────┐          │
│  Qdrant Server   │          │
│  (Docker)        │          │
└──────────────────┘          │
                              │
                              ▼
                       ┌──────────────┐
                       │   GPT-4o     │
                       └──────────────┘
```

---

## 🔄 State Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                    SYSTEM STATES                                │
└─────────────────────────────────────────────────────────────────┘

                    ┌─────────────┐
                    │   INITIAL   │
                    │  (No index) │
                    └──────┬──────┘
                           │
                           │ Run: python index.py
                           ▼
                    ┌─────────────┐
                    │  INDEXING   │
                    │ (In progress)│
                    └──────┬──────┘
                           │
                ┌──────────┼──────────┐
                │                     │
         ERROR  │                     │ SUCCESS
                ▼                     ▼
         ┌─────────────┐       ┌─────────────┐
         │   FAILED    │       │   INDEXED   │
         │ (Retry req) │       │  (Ready)    │
         └─────────────┘       └──────┬──────┘
                                      │
                                      │ Run: python chat.py
                                      ▼
                               ┌─────────────┐
                               │  CONNECTED  │
                               │ (Waiting)   │
                               └──────┬──────┘
                                      │
                                      │ User enters query
                                      ▼
                               ┌─────────────┐
                               │ RETRIEVING  │
                               │ (Searching) │
                               └──────┬──────┘
                                      │
                                      │ Chunks found
                                      ▼
                               ┌─────────────┐
                               │ GENERATING  │
                               │ (LLM call)  │
                               └──────┬──────┘
                                      │
                                      │ Answer ready
                                      ▼
                               ┌─────────────┐
                               │  COMPLETE   │
                               │ (Displayed) │
                               └──────┬──────┘
                                      │
                                      │ Loop back
                                      ▼
                               ┌─────────────┐
                               │  CONNECTED  │
                               │ (Waiting)   │
                               └─────────────┘
```

---

**Version**: 1.0  
**Last Updated**: January 2026
