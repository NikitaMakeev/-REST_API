from sqlalchemy import Column, Integer, String
from config.database import Base
import bcrypt

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(30), nullable=False, unique=True)
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String(255), nullable=False)

    @staticmethod
    def hash_password(password: str) -> str:
        """Хеширование пароля с помощью bcrypt"""
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def verify_password(self, password: str) -> bool:
        """Проверка пароля"""
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))