from fastapi import FastAPI

from app.database.init_db import init_db
from app.api.v1.datasets import router as datasets_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="InsightAI API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
         "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(datasets_router)

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