from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.user_routes import router as user_router
from routes.landmark_routes import router as landmark_router  # ✅ добавляем импорт
from routes.photo_routes import router as photo_router
from routes.rating_routes import router as rating_router

from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение роутов
app.include_router(user_router, tags=["Users"])          # ✅ Users
app.include_router(landmark_router, tags=["Landmarks"])  # ✅ Landmarks
app.include_router(photo_router, tags=["Photos"]) # ✅ Photo
app.include_router(rating_router, tags=["Ratings"])

@app.get("/")
def root():
    return {"message": "Сервер работает 🟢"}

# Запуск: uvicorn main:app --reload
