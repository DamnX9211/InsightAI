from fastapi import FastAPI

from app.database.init_db import init_db

app = FastAPI(title="InsightAI API")

@app.on_event("startup")
def on_startup():
    """
    Runs once when the FastAPI application starts.
    Creates database tables if they don't already exist.
    """
    init_db()


@app.get("/")
def root():
    return {
"message": "InsightAI Backend Running"
    }