from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.resources import Resource
from app.models.user import User
from app.schemas.resources import ResourceCreate, ResourceResponse
from app.core.security import get_current_user


router = APIRouter(
    prefix="/resources",
    tags=["Resources"]
)


@router.post("/", response_model=ResourceResponse)
def create_resource(
    resource_data: ResourceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_resource = Resource(
        title=resource_data.title,
        description=resource_data.description,
        resource_type=resource_data.resource_type,
        file_url=resource_data.file_url,
        owner_id=current_user.id
    )

    db.add(new_resource)
    db.commit()
    db.refresh(new_resource)

    return new_resource


@router.get("/", response_model=list[ResourceResponse])
def get_resources(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(Resource).all()


@router.get("/{resource_id}", response_model=ResourceResponse)
def get_resource(
    resource_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    resource = db.query(Resource).filter(
        Resource.id == resource_id
    ).first()

    if not resource:
        raise HTTPException(
            status_code=404,
            detail="Resource not found"
        )

    return resource