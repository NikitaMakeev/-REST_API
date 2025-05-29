from sqlalchemy.orm import relationship
from models.user import User
from models.landmark import Landmark
from models.photo import Photo
from models.rating import Rating

# Ассоциации

# Один пользователь имеет много:
User.photos = relationship("Photo", back_populates="user", cascade="all, delete-orphan")
User.ratings = relationship("Rating", back_populates="user", cascade="all, delete-orphan")
User.landmarks = relationship("Landmark", back_populates="user", cascade="all, delete-orphan")

# Landmark -> Photo, Rating
Landmark.photos = relationship("Photo", back_populates="landmark", cascade="all, delete-orphan")
Landmark.ratings = relationship("Rating", back_populates="landmark", cascade="all, delete-orphan")
Landmark.user = relationship("User", back_populates="landmarks")

# Photo: принадлежит пользователю и достопримечательности
Photo.user = relationship("User", back_populates="photos")
Photo.landmark = relationship("Landmark", back_populates="photos")

# Rating: принадлежит пользователю и достопримечательности
Rating.user = relationship("User", back_populates="ratings")
Rating.landmark = relationship("Landmark", back_populates="ratings")
