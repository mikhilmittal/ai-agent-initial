from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from quiz_generator import generate_question

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict to your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/quiz")
def get_question(topic: str = Query(...)):
    try:
        question_data = generate_question(topic)
        return question_data
    except Exception as e:
        return {"error": str(e)}
