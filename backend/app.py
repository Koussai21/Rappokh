"""FastAPI application for Rappokh"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, List
from backend.config import settings
from backend.report_gen.generator import ReportGenerator

app = FastAPI(
    title="Rappokh API",
    description="AI-Powered Report Generator",
    version="0.1.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize generator
generator = ReportGenerator()

# Models
class BrainstormRequest(BaseModel):
    initial_notes: str

class ClarificationAnswersRequest(BaseModel):
    brainstorm_notes: str
    answers: Dict[str, str]

class ReportRequest(BaseModel):
    brainstorm_notes: str
    answers: Optional[Dict[str, str]] = None

@app.get("/")
async def root():
    return {"message": "Bienvenue à Rappokh - AI Report Generator"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.post("/api/report/brainstorm")
async def start_brainstorm(request: BrainstormRequest):
    """Débuter une session de brainstorming"""
    try:
        result = generator.start_brainstorming_session(request.initial_notes)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/report/clarify")
async def get_clarifications(request: BrainstormRequest):
    """Obtenir des questions de clarification"""
    try:
        questions = generator.clarification_agent.ask_clarification_questions(
            request.initial_notes
        )
        return {
            "questions": questions,
            "round": generator.clarification_agent.clarifications_asked,
            "max_rounds": generator.clarification_agent.max_rounds
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/report/generate")
async def generate_report(request: ReportRequest):
    """Générer le rapport complet"""
    try:
        report = generator.generate_full_report(
            request.brainstorm_notes,
            request.answers
        )
        return {
            "status": "success",
            "report": report
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/report/evaluate")
async def evaluate_completeness(request: BrainstormRequest):
    """Évaluer la complétude des informations"""
    try:
        evaluation = generator.clarification_agent.evaluate_content_completeness(
            request.initial_notes
        )
        return evaluation
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )
