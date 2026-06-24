import os
from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

BASE_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BASE_DIR / ".env")

app = FastAPI()

templates = Jinja2Templates(directory="src/templates")


@app.get("/")
def home(request: Request):
    backend_url = os.getenv("BACKEND_URL", "http://localhost:8001")

    return templates.TemplateResponse(
        request=request,
        name="chat_page.html",
        context={"backend_url": backend_url},
    )
