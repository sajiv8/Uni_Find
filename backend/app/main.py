from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.database.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate

app = FastAPI()

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


@app.get("/")
def root():
    return {
        "message": "Uni_Find Backend Running"
    }


@app.get("/users")
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users


@app.post("/users")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    hashed_password = pwd_context.hash(user.password)

    new_user = User(
        name=user.name,
        email=user.email,
        password_hash=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
