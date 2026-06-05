from fastapi import FastAPI
from sqlalchemy import text
from app.database import engine
from app.cache import redis_client

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

@app.get("/db-health")
def db_health():

    try:

        with engine.connect() as conn:

            conn.execute(text("SELECT 1"))

        return {
            "database": "connected"
        }

    except Exception as e:

        return {
            "database": "failed",
            "error": str(e)
        }


@app.get("/cache-health")
def cache_health():

    try:

        redis_client.ping()

        return {
            "redis": "connected"
        }

    except Exception as e:

        return {
            "redis": "failed",
            "error": str(e)
        }