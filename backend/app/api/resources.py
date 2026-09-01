from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.user import User
from app.core.security import get_current_user


router = APIRouter(
    prefix="/resources",
    tags=["Resources"]
)


@router.get("/")
def get_resources(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return {
        "message": "Resources endpoint working",
        "user_id": current_user.id,
        "user_name": current_user.name
    }