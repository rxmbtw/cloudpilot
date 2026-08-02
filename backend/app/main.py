from fastapi import FastAPI, Depends, HTTPException

from fastapi import Request
import time

from app.security import (
    verify_access_token,
    verify_refresh_token,
    create_access_token,
    create_refresh_token,
)

from app.schemas.user import TokenResponse
from app.schemas.user import RefreshTokenRequest


from app.schemas.user import UserCreate, UserResponse, UserLogin
from app import crud

from app.models.user import User
from app.security import require_admin

from app.rate_limit import rate_limit
from app.logger import logger


from app.database import engine, get_db
from app.cache import redis_client
from sqlalchemy import text
from sqlalchemy.orm import Session
from prometheus_fastapi_instrumentator import Instrumentator

from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):

    email = verify_access_token(token)

    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user


app = FastAPI(title="CloudPilot API", version="0.1.0")


@app.middleware("http")
async def log_requests(request: Request, call_next):

    start_time = time.time()

    response = await call_next(request)

    process_time = round(time.time() - start_time, 4)

    logger.info(
        f"IP={request.client.host} "
        f"Method={request.method} "
        f"Path={request.url.path} "
        f"Status={response.status_code} "
        f"Time={process_time}s"
    )

    return response


Instrumentator().instrument(app).expose(app)


@app.get("/")
def root():

    return {"project": "CloudPilot", "status": "running", "version": "0.2.0"}


@app.get("/health")
def health():

    return {"status": "healthy"}


@app.get("/db-health")
def db_health():

    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))

        return {"database": "connected"}

    except Exception as e:
        return {"database": "failed", "error": str(e)}


@app.get("/cache-health")
def cache_health():

    try:
        redis_client.ping()

        return {"redis": "connected"}

    except Exception as e:
        return {"redis": "failed", "error": str(e)}


@app.get(
    "/admin/users",
    dependencies=[Depends(rate_limit)],
    response_model=list[UserResponse],
)
def admin_get_users(
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    require_admin(current_user)

    return crud.get_users(db)


@app.post("/users", response_model=UserResponse, dependencies=[Depends(rate_limit)])
def create_user(user: UserCreate, db: Session = Depends(get_db)):

    return crud.create_user(db, user)


@app.get(
    "/users", dependencies=[Depends(rate_limit)], response_model=list[UserResponse]
)
def get_users(
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):

    return crud.get_users(db)


@app.get(
    "/users/{user_id}", dependencies=[Depends(rate_limit)], response_model=UserResponse
)
def get_user(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")

    return crud.get_user(db, user_id)


@app.put(
    "/users/{user_id}", dependencies=[Depends(rate_limit)], response_model=UserResponse
)
def update_user(
    user_id: int,
    user: UserCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")

    return crud.update_user(db, user_id, user)


@app.delete("/users/{user_id}", dependencies=[Depends(rate_limit)])
def delete_user(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")

    return crud.delete_user(db, user_id)


@app.post(
    "/login",
    response_model=TokenResponse,
    # dependencies=[Depends(rate_limit)]
)
def login(user: UserLogin, db: Session = Depends(get_db)):

    logger.info(f"Login attempt: {user.email}")

    db_user = crud.authenticate_user(db, user.email, user.password)

    if not db_user:
        logger.warning(f"Failed login: {user.email}")

        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token({"sub": db_user.email, "role": db_user.role})

    refresh_token = create_refresh_token({"sub": db_user.email})

    logger.info(f"Successful login: {user.email}")

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@app.post("/refresh")
def refresh_token(token_data: RefreshTokenRequest):

    email = verify_refresh_token(token_data.refresh_token)

    access_token = create_access_token({"sub": email})

    return {"access_token": access_token, "token_type": "bearer"}
