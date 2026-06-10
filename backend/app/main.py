import importlib
try:
    fastapi_mod = importlib.import_module("fastapi")
    Depends = fastapi_mod.Depends
    FastAPI = fastapi_mod.FastAPI
except Exception:  # pragma: no cover - fallback when fastapi is unavailable (lint/runtime safety)
    # Minimal no-op fallbacks so the module can be imported when fastapi isn't installed.
    def Depends(x=None):
        return x

    class FastAPI:  # minimal stub
        def __init__(self, *args, **kwargs):
            pass
from sqlalchemy import text

from app.database import Base, engine, get_db
from app.cache import redis_client

try:
    Instrumentator = importlib.import_module("prometheus_fastapi_instrumentator").Instrumentator
except Exception:  # pragma: no cover - fallback when package is unavailable
    class Instrumentator:  # minimal no-op fallback for linting/runtime safety
        def __init__(self, *args, **kwargs):
            pass

        def instrument(self, app):
            return self

        def expose(self, app, **kwargs):
            return None

from app.models.user import User
from app.schemas.user import UserCreate, UserResponse
from app import crud
from sqlalchemy.orm import Session

from app.schemas.user import UserCreate
from app.schemas.user import UserResponse

from app import crud

app = FastAPI(
    title="CloudPilot API",
    version="0.1.0"
)

Base.metadata.create_all(bind=engine)
Instrumentator().instrument(app).expose(app)

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

@app.post("/users", response_model=UserResponse)
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):

    return crud.create_user(
        db,
        user
    )

@app.get("/users")
def get_users(
    db: Session = Depends(get_db)
):

    return crud.get_users(db)

@app.get("/users/{user_id}")
def get_user(
    user_id: int,
    db: Session = Depends(get_db)
):

    return crud.get_user(
        db,
        user_id
    )

@app.put("/users/{user_id}")
def update_user(
    user_id: int,
    user: UserCreate,
    db: Session = Depends(get_db)
):

    return crud.update_user(
        db,
        user_id,
        user
    )

@app.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db)
):

    return crud.delete_user(
        db,
        user_id
    )

