from pydantic import BaseModel
from typing import Optional

class PhotoBase(BaseModel):
    url: str
    description: Optional[str] = None
    landmark_id: int

class PhotoCreate(PhotoBase):
    pass

class PhotoUpdate(BaseModel):
    url: Optional[str]
    description: Optional[str]
    # landmark_id: Optional[int]

class PhotoResponse(PhotoBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True  # Для Pydantic v2
