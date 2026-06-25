from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware
import sys

from fastapi import FastAPI
from pydantic import BaseModel

#Add the project root folder so python can access week_3
PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.append(str(PROJECT_ROOT))

from week_2.find_skill_gaps import find_skill_gaps_from_text

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:8000",
        "http://localhost:8000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    resume_text: str = ""

@app.get("/")
def health_check():
    return{"status", "Backend is running"}

@app.post("/chat")
def chat(request: ChatRequest):
    database_path = PROJECT_ROOT / "week_2" / "data"/ "jobs_d1.db"

    result = find_skill_gaps_from_text(
        resume_text=request.resume_text,
        db_url=str(database_path),
    )

    if not request.resume_text.strip():
        return{
            "reply": "please upload a resume pdf first",
            "gaps": []
        }
    
    if result.gaps:
        gap_text = ", ".join(result.gaps[:10])

        return {
            "reply": f"Based on your resume, some skill gaps are : {gap_text}.",
            "gaps": result.gaps,
        }
    
    return {
        "reply" : "Great! No skill gaps were found from the available job-market skills.",
        "gaps": [],
    }