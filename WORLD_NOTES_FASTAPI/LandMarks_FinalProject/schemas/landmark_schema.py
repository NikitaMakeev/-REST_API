from pydantic import BaseModel
from typing import Optional

class LandmarkBase(BaseModel):
    name: str
    description: str
    location: str
    country: str
    imageURL: Optional[str] = None

class LandmarkCreate(LandmarkBase):
    pass

class LandmarkUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]
    location: Optional[str]
    country: Optional[str]
    imageURL: Optional[str]

class LandmarkResponse(LandmarkBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True
