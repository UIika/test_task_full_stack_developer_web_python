import logging
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.database import sqlite_engine
from src.core.config import settings
from src.schemas.users import UserCreateAdmin
from src.crud import users


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def init():
    async with AsyncSession(sqlite_engine) as session:
        if not await users.get_user_by_email(session, settings.FIRST_SUPERUSER_EMAIL):
            logger.info("Creating initial data")
            user = UserCreateAdmin(
                email=settings.FIRST_SUPERUSER_EMAIL,
                name=settings.FIRST_SUPERUSER_NAME,
                password=settings.FIRST_SUPERUSER_PASSWORD,
                is_superuser=True
            )
            await users.create(session, user)
        else:
            logger.info("Initial data already exists")
            
if __name__ == '__main__':
    asyncio.run(init())