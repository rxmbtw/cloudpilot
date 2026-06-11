from fastapi import (
    FastAPI,
    Depends,
    HTTPException
)

from app.security import verify_token
from app.models.user import User

from app.database import (
    Base,
    engine,
    get_db
)

from sqlalchemy import text
from sqlalchemy.orm import Session
from prometheus_fastapi_instrumentator import Instrumentator

from fastapi.security import OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="login"
)

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):

    email = verify_token(token)

    user = db.query(User).filter(
        User.email == email
    ).first()

    if not user:

        raise HTTPException(
            status_code=401,
            detail="User not found"
        )

    return user





from app.cache import redis_client

from app.schemas.user import (
    UserCreate,
    UserResponse,
    UserLogin,
    Token
)

from app.security import create_access_token

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
    current_user: User = Depends(get_current_user),
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


@app.post(
    "/login",
    response_model=Token
)
def login(
    user: UserLogin,
    db: Session = Depends(get_db)
):

    db_user = crud.authenticate_user(
        db,
        user.email,
        user.password
    )

    if not db_user:

        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    access_token = create_access_token(
        {
            "sub": db_user.email
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

