from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from config.database import Base

class Landmark(Base):
    __tablename__ = 'landmarks'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    location = Column(String(100), nullable=False)
    country = Column(String(50), nullable=False)
    imageURL = Column(String(100), nullable=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
