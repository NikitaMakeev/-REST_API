from pydantic import BaseModel
from typing import Optional

class RatingBase(BaseModel):
    rating: int

class RatingCreate(RatingBase):
    pass

class RatingUpdate(RatingBase):
    pass

class RatingResponse(RatingBase):
    id: int
    user_id: int
    landmark_id: int

    class Config:
        from_attributes = True
