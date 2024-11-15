from sqlalchemy.ext.asyncio import create_async_engine
from src.core.config import settings
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


sqlite_engine = create_async_engine(settings.SQLITE_URL)