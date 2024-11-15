from typing import Annotated, AsyncGenerator
from fastapi import Depends, HTTPException, Request, status
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from src.core.database import sqlite_engine
from src.core.config import settings
from src.core.security import ENCODING_ALGORITHM

from src.models import User
import jwt
from jwt.exceptions import InvalidTokenError


def set_flash_message(request: Request, message: str):
    if 'flash_messages' not in request.session:
        request.session['flash_messages'] = []
    request.session['flash_messages'].append(message)

def get_flash_messages(request: Request):
    messages = request.session.pop('flash_messages', [])
    return messages


AsyncSessionMaker = sessionmaker(
    bind=sqlite_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_sqlite_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionMaker() as session:
        yield session
        
SqliteSessionDep = Annotated[AsyncSession, Depends(get_sqlite_db)]



class RequiresLoginException(Exception):
    pass

async def get_request_user(
    request: Request,
    session: SqliteSessionDep,
) -> User| None:
    token = request.session.get("access_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_307_TEMPORARY_REDIRECT,
            headers={'Location': '/login'})
    try:
        payload: dict = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[ENCODING_ALGORITHM]
        )
    except (InvalidTokenError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_307_TEMPORARY_REDIRECT,
            headers={'Location': '/login'})
    user = await session.get(User, payload.get('sub'))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_307_TEMPORARY_REDIRECT,
            headers={'Location': '/login'})
    return user

CurrentUser = Annotated[User, Depends(get_request_user)]


async def get_request_superuser(
    request: Request,
    session: SqliteSessionDep,
) -> User:
    user: User = await get_request_user(request, session)
    if not user.is_superuser:
        set_flash_message(request, 'You have no permission')
        raise HTTPException(
            status_code=status.HTTP_307_TEMPORARY_REDIRECT,
            headers={"Location": "/"}
        )
    return user
        
CurrentSuperUser = Annotated[User, Depends(get_request_superuser)]