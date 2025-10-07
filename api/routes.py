from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.llm_service import generate_completion

router = APIRouter(prefix="/api", tags=["llm"])

class ChatRequest(BaseModel):
    prompt: str
    max_tokens: int = 100
    temperature: float = 0.7

class ChatResponse(BaseModel):
    response: str
    model: str
    tokens_used: int

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Generate a completion using Groq LLM with full observability
    """
    try:
        result = await generate_completion(
            prompt=request.prompt,
            max_tokens=request.max_tokens,
            temperature=request.temperature
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}
