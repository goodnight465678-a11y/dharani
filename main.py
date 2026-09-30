from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

from explanation_module import explain_concept
from qna import answer_question
from quiz_module import generate_quiz
from summary_module import summarize_text
from learning_path import get_learning_recommendations

app = FastAPI(title="EduGenie", version="1.0.0", description="Gemini-powered learning assistant")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

class TextRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=20000)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/health")
async def health():
    return {"status": "ok", "service": "EduGenie"}

@app.post("/qa")
async def qa(payload: TextRequest):
    return {"answer": answer_question(payload.text)}

@app.post("/explain")
async def explain(payload: TextRequest):
    return {"explanation": explain_concept(payload.text)}

@app.post("/quiz")
async def quiz(payload: TextRequest):
    return {"quiz": generate_quiz(payload.text)}

@app.post("/summarize")
async def summarize(payload: TextRequest):
    return {"summary": summarize_text(payload.text)}

@app.post("/learn/recommendations")
async def learning_recommendations(payload: TextRequest):
    return {"recommendations": get_learning_recommendations(payload.text)}
