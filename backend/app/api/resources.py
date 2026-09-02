from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.resources import Resource
from app.models.user import User
from app.schemas.resources import ResourceCreate, ResourceResponse
from app.core.security import get_current_user


router = APIRouter(
    prefix="/resources",
    tags=["resources"]
)


# CREATE RESOURCE
@router.post("/", response_model=ResourceResponse)
def create_resource(
    resource_data: ResourceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    resource = Resource(
        title=resource_data.title,
        description=resource_data.description,
        owner_id=current_user.id,
        resource_type=resource_data.resource_type,
        file_url=resource_data.file_url
    )

    db.add(resource)
    db.commit()
    db.refresh(resource)

    return resource


# GET ALL RESOURCES
@router.get("/", response_model=list[ResourceResponse])
def get_resources(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    resources = db.query(Resource).all()

    return resources


# GET RESOURCE BY ID
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


# UPDATE RESOURCE
@router.put("/{resource_id}", response_model=ResourceResponse)
def update_resource(
    resource_id: int,
    resource_data: ResourceCreate,
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

    if resource.owner_id != current_user.id and current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="You can only update your own resource"
        )

    resource.title = resource_data.title
    resource.description = resource_data.description
    resource.resource_type = resource_data.resource_type
    resource.file_url = resource_data.file_url

    db.commit()
    db.refresh(resource)

    return resource


# DELETE RESOURCE
@router.delete("/{resource_id}")
def delete_resource(
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

    if resource.owner_id != current_user.id and current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="You can only delete your own resource"
        )

    db.delete(resource)
    db.commit()

    return {
        "message": "Resource deleted successfully"
    }