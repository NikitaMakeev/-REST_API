from sqlalchemy import Column, Integer, ForeignKey
from config.database import Base

class Rating(Base):
    __tablename__ = 'ratings'

    id = Column(Integer, primary_key=True, index=True)
    rating = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    landmark_id = Column(Integer, ForeignKey('landmarks.id'), nullable=False)
