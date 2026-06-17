from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate

from app.security import hash_password
from app.security import verify_password


def create_user(db: Session, user: UserCreate):

    db_user = User(
        name=user.name, email=user.email, hashed_password=hash_password(user.password)
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def get_users(db: Session):

    return db.query(User).all()


def get_user(db: Session, user_id: int):

    return db.query(User).filter(User.id == user_id).first()


def update_user(db: Session, user_id: int, user: UserCreate):

    db_user = db.query(User).filter(User.id == user_id).first()

    if not db_user:
        return None

    db_user.name = user.name
    db_user.email = user.email
    db_user.hashed_password = hash_password(user.password)

    db.commit()
    db.refresh(db_user)

    return db_user


def delete_user(db: Session, user_id: int):

    db_user = db.query(User).filter(User.id == user_id).first()

    if not db_user:
        return None

    db.delete(db_user)
    db.commit()

    return db_user


def authenticate_user(db: Session, email: str, password: str):

    user = db.query(User).filter(User.email == email).first()

    if not user:
        return None

    if not verify_password(password, user.hashed_password):
        return None

    return user
