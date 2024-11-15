from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models import File
from src.schemas.files import FileCreate


async def create(session: AsyncSession, file: FileCreate):
    file_dict: dict = file.model_dump()
    new_file = File(**file_dict)
    session.add(new_file)
    await session.commit()
    await session.refresh(new_file)
    return new_file

async def read(session: AsyncSession, public_only=True):
    statement = select(File)
    if public_only:
        statement = statement.where(File.is_private == False)
    files = [row[0] for row in (await session.execute(statement)).all()]
    return files