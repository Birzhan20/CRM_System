from sqlalchemy import Column, Integer, Enum, DateTime, func, String
from core.database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(50), unique=True, nullable=False)
    last_name = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    phone = Column(String, nullable=True)
    role = Column(String, nullable=False)
    created_at = Column(DateTime, default=func.now())
