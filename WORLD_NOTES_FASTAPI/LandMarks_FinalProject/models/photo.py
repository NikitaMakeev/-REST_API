from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from config.database import Base

class Photo(Base):
    __tablename__ = 'photos'

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String(255), nullable=False)  # <= длина указана
    description = Column(String(500), nullable=True)  # <= длину лучше тоже указать
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    landmark_id = Column(Integer, ForeignKey('landmarks.id'), nullable=False)
