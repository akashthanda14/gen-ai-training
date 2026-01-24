"""
Module 4: FastAPI Deployment with Async/Await and Streaming
============================================================
Build a real backend. Learn the CRITICAL concept of blocking vs non-blocking.

Key Concept: If you use 'def' (synchronous), one user waits for the previous
user's LLM to finish (10+ seconds). If you use 'async def', the server can
handle other traffic while waiting for the LLM.

This is REQUIRED for production LLM APIs!
"""

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from openai import AsyncOpenAI
import os
from dotenv import load_dotenv
import asyncio
import time

load_dotenv()

app = FastAPI(
    title="LLM API with Async/Await",
    description="Production-ready LLM API demonstrating async and streaming"
)

# Use AsyncOpenAI for non-blocking calls
client = AsyncOpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


# ============================================================================
# Example 1: The Problem - Synchronous (Blocking)
# ============================================================================

@app.post("/chat/sync")
def chat_sync(prompt: str):
    """
    ❌ BLOCKING ENDPOINT
    
    Problem: This blocks the entire server while waiting for OpenAI.
    If this takes 10 seconds, NO other requests can be processed!
    """
    print(f"[SYNC] Starting request at {time.time()}")
    
    # This BLOCKS the server for ~2-5 seconds
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    
    print(f"[SYNC] Finished request at {time.time()}")
    
    return {"response": response.choices[0].message.content}


# ============================================================================
# Example 2: The Solution - Asynchronous (Non-Blocking)
# ============================================================================

@app.post("/chat/async")
async def chat_async(prompt: str):
    """
    ✅ NON-BLOCKING ENDPOINT
    
    Solution: This uses 'async def' and 'await'.
    While waiting for OpenAI, the server can handle other requests!
    """
    print(f"[ASYNC] Starting request at {time.time()}")
    
    # This does NOT block - server can handle other requests
    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    
    print(f"[ASYNC] Finished request at {time.time()}")
    
    return {"response": response.choices[0].message.content}


# ============================================================================
# Example 3: Streaming Response (Real-Time)
# ============================================================================

async def generate_response(prompt: str):
    """
    Generator function that yields tokens as they arrive.
    
    This is what makes the response appear word-by-word in real-time!
    """
    stream = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        stream=True  # Enable streaming from OpenAI
    )
    
    async for chunk in stream:
        if chunk.choices[0].delta.content:
            # Yield each token as it arrives
            yield chunk.choices[0].delta.content


@app.post("/chat/stream")
async def chat_stream(prompt: str):
    """
    ✅ STREAMING ENDPOINT
    
    Returns tokens as they arrive (word-by-word).
    Much better user experience than waiting for full response!
    """
    # StreamingResponse passes chunks to the client as they arrive
    return StreamingResponse(
        generate_response(prompt),
        media_type="text/plain"
    )


# ============================================================================
# Example 4: Demonstration of Concurrent Handling
# ============================================================================

@app.get("/demo/concurrent")
async def demo_concurrent():
    """
    Demonstrates that async endpoints can handle multiple requests concurrently.
    
    This makes 3 LLM calls at the same time!
    """
    start_time = time.time()
    
    # Make 3 calls concurrently (not sequentially!)
    tasks = [
        client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": f"Count to {i}"}],
            max_tokens=20
        )
        for i in [3, 5, 7]
    ]
    
    # Wait for all to complete
    responses = await asyncio.gather(*tasks)
    
    end_time = time.time()
    
    return {
        "message": "Made 3 LLM calls concurrently!",
        "time_taken": f"{end_time - start_time:.2f} seconds",
        "responses": [r.choices[0].message.content for r in responses]
    }


# ============================================================================
# Teaching Endpoint: Compare Sync vs Async
# ============================================================================

@app.get("/demo/compare")
async def demo_compare():
    """
    Teaching demonstration: Shows the difference between sync and async.
    
    Try calling /chat/sync and /chat/async multiple times simultaneously
    and see the difference!
    """
    return {
        "sync_endpoint": "/chat/sync",
        "async_endpoint": "/chat/async",
        "streaming_endpoint": "/chat/stream",
        "explanation": {
            "sync": "Blocks server. Only one request at a time.",
            "async": "Non-blocking. Multiple requests handled concurrently.",
            "stream": "Returns tokens in real-time as they arrive."
        },
        "test_instructions": [
            "1. Open two terminals",
            "2. In both, run: curl -X POST http://localhost:8000/chat/sync -d 'prompt=Count to 100'",
            "3. Notice the second request waits for the first to finish",
            "4. Now try with /chat/async - both run concurrently!"
        ]
    }


# ============================================================================
# Health Check
# ============================================================================

@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "LLM API with Async/Await",
        "endpoints": {
            "/chat/sync": "Synchronous (blocking) - DON'T USE IN PRODUCTION",
            "/chat/async": "Asynchronous (non-blocking) - PRODUCTION READY",
            "/chat/stream": "Streaming response - BEST UX",
            "/demo/concurrent": "Demonstrates concurrent handling",
            "/demo/compare": "Comparison and testing instructions"
        },
        "docs": "/docs"
    }


# ============================================================================
# Teaching Points (Printed on Startup)
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Print teaching points when server starts."""
    print("\n" + "=" * 70)
    print("🎓 KEY TEACHING POINTS: Async/Await for LLMs")
    print("=" * 70)
    
    print("""
1. THE PROBLEM: BLOCKING CODE
   ---------------------------
   def chat(prompt):  # ❌ Synchronous
       response = client.chat.completions.create(...)
       return response
   
   When this runs:
   - Server makes API call to OpenAI
   - Waits 2-10 seconds for response
   - During this time, server is BLOCKED
   - No other requests can be processed!
   
   Result: Terrible performance, angry users

2. THE SOLUTION: ASYNC/AWAIT
   --------------------------
   async def chat(prompt):  # ✅ Asynchronous
       response = await client.chat.completions.create(...)
       return response
   
   When this runs:
   - Server makes API call to OpenAI
   - While waiting, server can handle OTHER requests
   - When response arrives, server resumes this request
   
   Result: Multiple users served concurrently!

3. HOW IT WORKS
   -------------
   'async def' = This function can be paused
   'await'     = Pause here, let others run
   
   Think of it like a restaurant:
   
   Synchronous (Bad):
   - Waiter takes order from Table 1
   - Waits in kitchen until food is ready
   - Brings food to Table 1
   - Only then takes order from Table 2
   
   Asynchronous (Good):
   - Waiter takes order from Table 1
   - While kitchen cooks, takes order from Table 2
   - When food ready, brings to Table 1
   - Continues serving multiple tables

4. STREAMING RESPONSES
   --------------------
   StreamingResponse(generate_response(prompt))
   
   Instead of:
   [wait 10 seconds] "Here is your complete answer..."
   
   User sees:
   "Here" [0.1s] "is" [0.1s] "your" [0.1s] "complete" [0.1s] "answer"
   
   Benefits:
   - User sees progress immediately
   - Feels much faster
   - Can stop if answer is wrong
   - Better UX

5. WHEN TO USE ASYNC
   ------------------
   ✅ LLM API calls (always!)
   ✅ Database queries
   ✅ External API calls
   ✅ File I/O
   ✅ Any I/O-bound operation
   
   ❌ CPU-intensive calculations
   ❌ Simple data processing

6. FASTAPI + ASYNC = PERFECT FOR LLMS
   ------------------------------------
   FastAPI has NATIVE async support.
   
   Flask/Django: Async is bolted on, not native
   FastAPI: Built for async from day one
   
   For LLM APIs, FastAPI is the best choice!

7. TESTING THE DIFFERENCE
   -----------------------
   Try this:
   
   Terminal 1:
   curl -X POST http://localhost:8000/chat/sync -d "prompt=Count to 100"
   
   Terminal 2 (immediately after):
   curl -X POST http://localhost:8000/chat/sync -d "prompt=Count to 50"
   
   Notice: Terminal 2 waits for Terminal 1 to finish!
   
   Now try with /chat/async - both run at the same time!

8. PRODUCTION REQUIREMENTS
   ------------------------
   For production LLM APIs, you MUST use:
   - async def (not def)
   - await (not blocking calls)
   - AsyncOpenAI (not OpenAI)
   - StreamingResponse (for better UX)
   
   Otherwise: Poor performance, unhappy users!
""")
    
    print("=" * 70)
    print("🚀 Server Started!")
    print("=" * 70)
    print("\n📚 API Documentation: http://localhost:8000/docs")
    print("🧪 Test Comparison: http://localhost:8000/demo/compare")
    print("\n✨ Try the streaming endpoint:")
    print("   curl -X POST http://localhost:8000/chat/stream \\")
    print("     -H 'Content-Type: application/json' \\")
    print("     -d '{\"prompt\": \"Write a haiku about coding\"}'")
    print()


# ============================================================================
# Main (for development)
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║         FastAPI LLM Server with Async/Await               ║
    ╚═══════════════════════════════════════════════════════════╝
    
    This server demonstrates:
    ✅ Async/await for non-blocking LLM calls
    ✅ Streaming responses for real-time output
    ✅ Concurrent request handling
    
    Starting server...
    """)
    
    uvicorn.run(
        "async_streaming:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
