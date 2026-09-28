from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
import httpx

app = FastAPI(
    title="Local AI Microservice",
    description="API RESTful to ask a local LLM (Qwen 2.5 7B) via Ollama.",
    version="1.0.0",
)

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen2.5:7b"




class PromptRequest(BaseModel):
    prompt: str = Field(..., min_length=2, description="The question or instruction for the model")
    system_prompt: str | None = Field(
        default="You are an exper assistant in backend and software",
        description="The context or role the model will get."
    )
    temperature: float = Field(default=0.7, ge=0.0, le=2.0, description="Creativity of answer (0=precise, 1=creative).")


class PromptResponse(BaseModel):
    model: str
    response: str
    total_duration_seconds: float




@app.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    """Verify if the API and Ollama are active."""
    try:
        async with httpx.AsyncClient(timeout=3.0) as client:
            res = await client.get("http://localhost:11434/")
            if res.status_code == 200:
                return {"status": "ok", "ollama": "connected"}
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Ollama is not answering in http://localhost:11434"
        )


@app.post("/generate", response_model=PromptResponse, status_code=status.HTTP_200_OK)
async def generate_response(payload: PromptRequest):
    """
    Send a local question to model Qwen 2.5
    """
    ollama_payload = {
        "model": MODEL_NAME,
        "prompt": payload.prompt,
        "system": payload.system_prompt,
        "stream": False,
        "options": {
            "temperature": payload.temperature
        }
    }

    try:
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(OLLAMA_URL, json=ollama_payload)
            
            if response.status_code != 200:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Ollama Error: {response.text}"
                )

            data = response.json()
            duration = data.get("total_duration", 0) / 1e9

            return PromptResponse(
                model=data.get("model", MODEL_NAME),
                response=data.get("response", "").strip(),
                total_duration_seconds=round(duration, 2)
            )

    except httpx.ReadTimeout:
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail="Model timeout"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal Server Error: {str(e)}"
        )