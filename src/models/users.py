from sqlalchemy import Column, Integer, String, Boolean
from src.core.database import Base


class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    email = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)
    downloads = Column(Integer, default=0, nullable=False)
