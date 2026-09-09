from fastapi import FastAPI, BackgroundTasks, HTTPException
from app.models import NFCPayload, RiskAssessmentResponse
from app.orchestrator import ArbiterOrchestrator

app = FastAPI(title="Arbiter Engine API", version="5.0")
orchestrator = ArbiterOrchestrator()

@app.post("/api/v1/scan", response_model=RiskAssessmentResponse)
async def process_nfc_scan(payload: NFCPayload, background_tasks: BackgroundTasks):
    try:
        payload_dict = payload.model_dump()
        
        # 1. Guard Clauses & Fast Eval (Instantly triggers UI logic)
        fast_eval_results = orchestrator.fast_eval(payload_dict)
        
        # 2. ReAct Agent Loop (Langchain & Llama-3) pushed to background
        background_tasks.add_task(orchestrator.deep_eval_react_loop, payload_dict, fast_eval_results)
        
        return {
            "entity_id": payload.entity_id,
            "status": "processing_in_background",
            "quick_flag": fast_eval_results["is_suspicious"],
            "message": "Initial heuristics complete. Llama-3 ReAct agent deployed."
        }
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))