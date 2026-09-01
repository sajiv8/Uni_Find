from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ResourceCreate(BaseModel):
    title: str
    description: str | None = None
    category: str
    location: str | None = None


class ResourceResponse(BaseModel):
    id: int
    title: str
    description: str | None
    category: str
    location: str | None
    is_available: bool
    owner_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)