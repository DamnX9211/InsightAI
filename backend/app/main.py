from fastapi import FastAPI

app = FastAPI(title="InsightAI API")

@app.get("/")
def root():
    return {
"message": "InsightAI Backend Running"
    }