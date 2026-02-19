from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.core.orchestration import Orchestrator
import uvicorn

app = FastAPI(title="CognitionOS API")

class TaskRequest(BaseModel):
    query: str

class TaskResponse(BaseModel):
    result: str

@app.on_event("startup")
async def startup_event():
    # Initialize global orchestrator or resources if needed
    pass

@app.post("/task", response_model=TaskResponse)
async def run_task(req: TaskRequest):
    orchestrator = Orchestrator()
    final_output = ""
    
    try:
        async for step in orchestrator.run_workflow(req.query):
            if "code_output" in step:
                final_output = step["code_output"]
                
        return TaskResponse(result=final_output)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
