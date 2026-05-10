from fastapi import FastAPI
from crew import run_crew

app = FastAPI()


@app.get("/")
def home():
    return {"message": "AI API Running"}


@app.post("/generate")
def generate(topic: str):
    result = run_crew(topic)

    return {
        "output": result.raw
    }