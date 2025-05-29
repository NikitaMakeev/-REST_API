# routes/landmark_routes.py
from fastapi import APIRouter, Depends
from controllers.landmark_controller import (
    get_all_landmarks_controller,
    get_landmark_controller,
    create_landmark_controller,
    update_landmark_controller,
    delete_landmark_controller,
)
from schemas.landmark_schema import LandmarkCreate, LandmarkUpdate, LandmarkResponse
from middleware.auth import get_current_user
from models.user import User

router = APIRouter()

@router.get("/landmarks", response_model=list[LandmarkResponse])
async def get_all_landmarks(country: str = None, sort: str = None):
    return await get_all_landmarks_controller(country, sort)

@router.get("/landmarks/{landmark_id}", response_model=LandmarkResponse)
async def get_landmark(landmark_id: int):
    return await get_landmark_controller(landmark_id)

@router.post("/landmarks", response_model=LandmarkResponse, status_code=201)
async def create_landmark(data: LandmarkCreate, user: User = Depends(get_current_user)):
    return await create_landmark_controller(data, user)

@router.put("/landmarks/{landmark_id}", response_model=LandmarkResponse)
async def update_landmark(landmark_id: int, data: LandmarkUpdate, user: User = Depends(get_current_user)):
    return await update_landmark_controller(landmark_id, data, user)

@router.delete("/landmarks/{landmark_id}", status_code=204)
async def delete_landmark(landmark_id: int, user: User = Depends(get_current_user)):
    return await delete_landmark_controller(landmark_id, user)
