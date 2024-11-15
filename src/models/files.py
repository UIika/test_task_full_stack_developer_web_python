from sqlalchemy import Column, Integer, String, Boolean, DateTime
from src.core.database import Base
from datetime import datetime, UTC

class File(Base):
    __tablename__ = 'files'
    
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    filename = Column(String, nullable=False)
    upload_time = Column(DateTime, default=datetime.now(UTC), nullable=False)
    downloads = Column(Integer, default=0, nullable=False)
    is_private = Column(Boolean, default=False, nullable=False)
    
