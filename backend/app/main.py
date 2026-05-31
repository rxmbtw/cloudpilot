from fastapi import FastAPI

app = FastAPI(
    title="CloudPilot API",
    version="0.1.0"
)

@app.get("/")
def root():
    return {
        "project": "CloudPilot",
        "status": "running",
        "version": "0.1.0"
    }

@app.get("/health")
def health():
    return {
        "status": "healthy"
    }