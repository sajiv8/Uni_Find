from pydantic import BaseModel
from typing import Optional


class ResourceCreate(BaseModel):
    title: str
    description: Optional[str] = None
    resource_type: str
    file_url: Optional[str] = None


class ResourceResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    owner_id: int
    resource_type: str
    file_url: Optional[str] = None

    class Config:
        from_attributes = True