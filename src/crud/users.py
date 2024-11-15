from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models import User
from src.schemas.users import UserCreate
from src.core.security import pwd_context, verify_password

async def get_user_by_email(session: AsyncSession, email: str) -> User|None:
    statement = select(User).where(User.email == email)
    user = (await session.execute(statement)).scalar_one_or_none()
    return user

async def read(session: AsyncSession):
    users = [row[0] for row in (await session.execute(select(User))).all()]
    return users

async def authenticate(session: AsyncSession, email: str, password: str) -> User|None:
    user = await get_user_by_email(session=session, email=email)
    if not user:
        return
    if not verify_password(password, user.hashed_password):
        return
    return user

async def create(session: AsyncSession, user: UserCreate):
    user: dict = user.model_dump()
    user['hashed_password'] = pwd_context.hash(user.pop('password'))
    new_user = User(**user)
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user