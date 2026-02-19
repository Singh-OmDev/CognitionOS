from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from src.core.orchestration import Orchestrator
import uvicorn
import json
import asyncio

app = FastAPI(title="CognitionOS API")

# Allow Frontend Access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TaskRequest(BaseModel):
    query: str

@app.on_event("startup")
async def startup_event():
    # Initialize global resources if needed
    pass

async def event_generator(query: str):
    """Generate Server-Sent Events from Orchestrator"""
    orchestrator = Orchestrator()
    
    try:
        async for step in orchestrator.run_workflow(query):
            # Format as SSE data
            json_data = json.dumps(step)
            yield f"data: {json_data}\n\n"
            
            # Small delay to ensure flush/avoid blocking
            await asyncio.sleep(0.01)
            
        # Signal completion
        yield "data: [DONE]\n\n"
        
    except Exception as e:
        error_data = json.dumps({"error": str(e)})
        yield f"data: {error_data}\n\n"

@app.post("/task/stream")
async def stream_task(req: TaskRequest):
    return StreamingResponse(
        event_generator(req.query),
        media_type="text/event-stream"
    )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
