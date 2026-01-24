"""
16. FastAPI LLM Endpoints
==========================
Demonstrates how to create production-ready API endpoints for LLMs
using FastAPI.

Key Concepts:
- RESTful API design for LLMs
- Request/response models with Pydantic
- Streaming responses
- Error handling
- Rate limiting
- Authentication

Prerequisites:
pip install fastapi uvicorn python-dotenv openai pydantic slowapi
"""

from fastapi import FastAPI, HTTPException, Depends, status, Request
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum
import os
from dotenv import load_dotenv
from openai import OpenAI
import json
import time
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="LLM API",
    description="Production-ready LLM API with OpenAI integration",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Rate limiting
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# ============================================================================
# Pydantic Models
# ============================================================================

class ModelType(str, Enum):
    """Available LLM models."""
    GPT4O = "gpt-4o"
    GPT4O_MINI = "gpt-4o-mini"
    GPT35_TURBO = "gpt-3.5-turbo"


class Message(BaseModel):
    """Chat message."""
    role: str = Field(..., description="Message role: system, user, or assistant")
    content: str = Field(..., description="Message content")


class ChatRequest(BaseModel):
    """Chat completion request."""
    messages: List[Message] = Field(..., description="List of messages")
    model: ModelType = Field(ModelType.GPT4O_MINI, description="Model to use")
    temperature: float = Field(0.7, ge=0.0, le=2.0, description="Sampling temperature")
    max_tokens: Optional[int] = Field(None, description="Maximum tokens to generate")
    stream: bool = Field(False, description="Enable streaming response")


class ChatResponse(BaseModel):
    """Chat completion response."""
    response: str = Field(..., description="Generated response")
    model: str = Field(..., description="Model used")
    usage: Dict[str, int] = Field(..., description="Token usage")
    finish_reason: str = Field(..., description="Reason for completion")


class CompletionRequest(BaseModel):
    """Simple completion request."""
    prompt: str = Field(..., description="Input prompt")
    model: ModelType = Field(ModelType.GPT4O_MINI, description="Model to use")
    temperature: float = Field(0.7, ge=0.0, le=2.0)
    max_tokens: int = Field(100, ge=1, le=4000)


class CompletionResponse(BaseModel):
    """Simple completion response."""
    completion: str
    model: str
    tokens_used: int


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    timestamp: float
    version: str


# ============================================================================
# Authentication
# ============================================================================

async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Verify API token.
    In production, implement proper token validation.
    """
    token = credentials.credentials
    
    # Simple token check (replace with proper validation)
    valid_token = os.getenv("API_TOKEN", "demo-token-12345")
    
    if token != valid_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token"
        )
    
    return token


# ============================================================================
# Endpoints
# ============================================================================

@app.get("/", response_model=HealthResponse)
async def root():
    """Root endpoint with API information."""
    return HealthResponse(
        status="online",
        timestamp=time.time(),
        version="1.0.0"
    )


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        timestamp=time.time(),
        version="1.0.0"
    )


@app.post("/api/v1/chat", response_model=ChatResponse)
@limiter.limit("10/minute")
async def chat_completion(
    request: Request,
    chat_request: ChatRequest,
    token: str = Depends(verify_token)
):
    """
    Chat completion endpoint.
    
    - **messages**: List of chat messages
    - **model**: LLM model to use
    - **temperature**: Sampling temperature (0.0-2.0)
    - **max_tokens**: Maximum tokens to generate
    - **stream**: Enable streaming (not supported in this endpoint)
    """
    try:
        # Convert Pydantic models to dict
        messages = [msg.dict() for msg in chat_request.messages]
        
        # Call OpenAI API
        response = client.chat.completions.create(
            model=chat_request.model.value,
            messages=messages,
            temperature=chat_request.temperature,
            max_tokens=chat_request.max_tokens
        )
        
        # Extract response
        message = response.choices[0].message
        usage = response.usage
        
        return ChatResponse(
            response=message.content,
            model=response.model,
            usage={
                "prompt_tokens": usage.prompt_tokens,
                "completion_tokens": usage.completion_tokens,
                "total_tokens": usage.total_tokens
            },
            finish_reason=response.choices[0].finish_reason
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating response: {str(e)}"
        )


@app.post("/api/v1/chat/stream")
@limiter.limit("5/minute")
async def chat_completion_stream(
    request: Request,
    chat_request: ChatRequest,
    token: str = Depends(verify_token)
):
    """
    Streaming chat completion endpoint.
    Returns Server-Sent Events (SSE) stream.
    """
    try:
        messages = [msg.dict() for msg in chat_request.messages]
        
        def generate():
            """Generator for streaming response."""
            stream = client.chat.completions.create(
                model=chat_request.model.value,
                messages=messages,
                temperature=chat_request.temperature,
                max_tokens=chat_request.max_tokens,
                stream=True
            )
            
            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    content = chunk.choices[0].delta.content
                    # Send as SSE format
                    yield f"data: {json.dumps({'content': content})}\n\n"
            
            # Send completion signal
            yield f"data: {json.dumps({'done': True})}\n\n"
        
        return StreamingResponse(
            generate(),
            media_type="text/event-stream"
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error streaming response: {str(e)}"
        )


@app.post("/api/v1/completion", response_model=CompletionResponse)
@limiter.limit("20/minute")
async def simple_completion(
    request: Request,
    completion_request: CompletionRequest,
    token: str = Depends(verify_token)
):
    """
    Simple completion endpoint.
    
    - **prompt**: Input text prompt
    - **model**: LLM model to use
    - **temperature**: Sampling temperature
    - **max_tokens**: Maximum tokens to generate
    """
    try:
        response = client.chat.completions.create(
            model=completion_request.model.value,
            messages=[
                {"role": "user", "content": completion_request.prompt}
            ],
            temperature=completion_request.temperature,
            max_tokens=completion_request.max_tokens
        )
        
        return CompletionResponse(
            completion=response.choices[0].message.content,
            model=response.model,
            tokens_used=response.usage.total_tokens
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating completion: {str(e)}"
        )


@app.get("/api/v1/models")
async def list_models(token: str = Depends(verify_token)):
    """List available models."""
    return {
        "models": [
            {
                "id": model.value,
                "name": model.name,
                "description": f"{model.value} model"
            }
            for model in ModelType
        ]
    }


# ============================================================================
# Error Handlers
# ============================================================================

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Custom HTTP exception handler."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "message": exc.detail,
                "type": "http_error",
                "code": exc.status_code
            }
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """General exception handler."""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": {
                "message": "Internal server error",
                "type": "server_error",
                "code": 500
            }
        }
    )


# ============================================================================
# Startup/Shutdown Events
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Run on application startup."""
    print("🚀 LLM API starting up...")
    print(f"📝 API Documentation: http://localhost:8000/docs")
    print(f"🔒 Authentication: Bearer token required")
    print(f"⚡ Rate limiting: Enabled")


@app.on_event("shutdown")
async def shutdown_event():
    """Run on application shutdown."""
    print("👋 LLM API shutting down...")


# ============================================================================
# Main (for development)
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║                    LLM FastAPI Server                     ║
    ╚═══════════════════════════════════════════════════════════╝
    
    📚 Documentation: http://localhost:8000/docs
    🔄 ReDoc: http://localhost:8000/redoc
    
    🔑 API Token: demo-token-12345
    
    Example cURL request:
    
    curl -X POST http://localhost:8000/api/v1/completion \\
      -H "Authorization: Bearer demo-token-12345" \\
      -H "Content-Type: application/json" \\
      -d '{
        "prompt": "What is FastAPI?",
        "model": "gpt-4o-mini",
        "max_tokens": 100
      }'
    
    Starting server...
    """)
    
    uvicorn.run(
        "16_fastapi_llm_endpoint:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
