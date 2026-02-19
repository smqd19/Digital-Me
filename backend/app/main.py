"""
Digital Avatar Chatbot - FastAPI Backend

A RAG-powered chatbot that serves as Qasim's digital avatar,
answering questions about his experience, projects, and skills.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import json

from .config import get_settings
from .models import ChatRequest, ChatResponse, HealthResponse
from .retrieval import VectorStore
from .agents import ChatAgent


# Global instances
vector_store: VectorStore | None = None
chat_agent: ChatAgent | None = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize and cleanup resources."""
    global vector_store, chat_agent
    
    settings = get_settings()
    
    if not settings.openai_api_key:
        print("WARNING: OPENAI_API_KEY not set. API will not function correctly.")
    else:
        # Initialize vector store
        vector_store = VectorStore(
            persist_directory=settings.chroma_persist_directory,
            knowledge_base_path=settings.knowledge_base_path,
            openai_api_key=settings.openai_api_key,
            embedding_model=settings.embedding_model
        )
        
        # Initialize chat agent
        chat_agent = ChatAgent(
            openai_api_key=settings.openai_api_key,
            model_name=settings.model_name,
            vector_store=vector_store
        )
        
        print("Digital Avatar Backend initialized successfully!")
    
    yield
    
    # Cleanup
    print("Shutting down...")


app = FastAPI(
    title="Digital Avatar API",
    description="AI-powered chatbot representing Qasim Sheikh's professional profile",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
settings = get_settings()
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", response_model=HealthResponse)
async def root():
    """Root endpoint with API info."""
    return HealthResponse(
        status="online",
        message="Digital Avatar API is running. Visit /docs for API documentation."
    )


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    if chat_agent is None:
        return HealthResponse(
            status="degraded",
            message="Chat agent not initialized. Check OPENAI_API_KEY."
        )
    return HealthResponse(status="healthy", message="All systems operational.")


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Send a message to the digital avatar and get a response.
    
    The avatar uses RAG to search through Qasim's experience, projects,
    and skills to provide accurate, personalized responses.
    """
    if chat_agent is None:
        raise HTTPException(
            status_code=503,
            detail="Chat service not available. Please check API configuration."
        )
    
    try:
        response, sources = chat_agent.chat(
            user_message=request.message,
            conversation_history=request.conversation_history
        )
        
        return ChatResponse(response=response, sources=sources)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    """
    Stream a response from the digital avatar.
    
    Returns a Server-Sent Events stream for real-time response display.
    """
    if chat_agent is None:
        raise HTTPException(
            status_code=503,
            detail="Chat service not available. Please check API configuration."
        )
    
    async def generate():
        try:
            for chunk in chat_agent.chat_stream(
                user_message=request.message,
                conversation_history=request.conversation_history
            ):
                # SSE format
                yield f"data: {json.dumps({'content': chunk})}\n\n"
            
            yield "data: [DONE]\n\n"
        
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"
    
    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        }
    )


@app.post("/reindex")
async def reindex_knowledge_base():
    """
    Force reindex of the knowledge base.
    
    Use this endpoint after updating the knowledge_base.json file.
    """
    if vector_store is None:
        raise HTTPException(
            status_code=503,
            detail="Vector store not available."
        )
    
    try:
        vector_store.reindex()
        return {"status": "success", "message": "Knowledge base reindexed successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
