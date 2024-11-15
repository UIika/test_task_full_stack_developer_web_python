import os
from typing import Union
from fastapi import APIRouter, Form, Header, Request, UploadFile
from fastapi.templating import Jinja2Templates
from src.models import File, User
from src.schemas.files import FileCreate
from src.schemas.users import UserCreate
from fastapi.responses import FileResponse, RedirectResponse
from src.deps import CurrentUser, CurrentSuperUser, SqliteSessionDep, get_flash_messages, set_flash_message
from src.crud import users, files
from src.core.security import create_access_token
from pydantic import ValidationError
from datetime import datetime, timedelta
import aiofiles
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('')


router = APIRouter(
    prefix='',
    tags=['Pages']
)


templates = Jinja2Templates(directory='src/templates')
templates.env.globals['get_flash_messages'] = get_flash_messages



@router.get('/')
async def files_page(request: Request, session: SqliteSessionDep, current_user: CurrentUser):
    all_files = await files.read(session, (not current_user.is_superuser))
    return templates.TemplateResponse(
        'files.html',
        {
            'request': request,
            'current_user': current_user,
            'all_files': all_files
        }
    )
        
@router.get('/users')
async def users_page(request: Request, session: SqliteSessionDep, current_user: CurrentSuperUser):
    all_users = await users.read(session)
    print(all_users)
    return templates.TemplateResponse('users.html', {
        'request': request, 'all_users': all_users, 'current_user': current_user
    })



@router.get('/signup')
async def signup(request: Request):
    return templates.TemplateResponse('signup.html',{'request': request})

@router.post('/signup')
async def signup(request: Request, session: SqliteSessionDep):
    user_data = dict(await request.form())
    
    if user_data.get('password') != user_data.get('password1'):
        set_flash_message(request, 'Passwords do not match')
        return RedirectResponse('/signup', status_code=303)
        
    user_data.pop('password1')
    
    try:
        user_to_create = UserCreate(**user_data)
    except ValidationError:
        set_flash_message(request, 'Invalid email')
        return RedirectResponse('/signup', status_code=303)

    user = await users.get_user_by_email(session, user_data.get('email'))
    if user:
        set_flash_message(request, 'User with such email already exists')
        return RedirectResponse('/signup', status_code=303)

    new_user = await users.create(session, user_to_create)
    print(new_user.is_superuser)
    return RedirectResponse('/login', status_code=303)


@router.get('/login')
async def login(request: Request):
    return templates.TemplateResponse('login.html',{'request': request})

@router.post('/login')
async def login(request: Request, session: SqliteSessionDep):
    user_data = dict(await request.form())
    
    user = await users.authenticate(session, **user_data)
    if not user:
        set_flash_message(request, 'Wrong email or password')
        return RedirectResponse('/login', status_code=303)

    access_token_expires = timedelta(minutes=60) # jwt token in session expires in 60 minutes
    access_token=create_access_token(
            subject=user.id, expires_delta=access_token_expires
        )
    request.session['access_token'] = access_token
    
    return RedirectResponse('/', status_code=303)


@router.get('/logout')
async def logout(request: Request, current_user: CurrentUser):
    request.session.clear()
    return RedirectResponse('/', status_code=303)


@router.post('/upload')
async def upload(
    request: Request,
    current_user: CurrentSuperUser,
    session: SqliteSessionDep,
    file: UploadFile = File(),
    is_private: Union[str, None] = Form(None),
    content_length: int = Header(...)
):  
    if not file.filename:
        set_flash_message(request, 'No file chosen')
        return RedirectResponse('/', status_code=303)
    
    if content_length>52_428_800: # 50MB
        set_flash_message(request, 'File is too large')
        return RedirectResponse('/', status_code=303)

    destination_path = f'src/static/files/{file.filename}'

    if not os.path.exists('src/static/files/'):
        os.makedirs('src/static/files/')

    if not os.path.exists(destination_path):
        await files.create(session, FileCreate(filename=file.filename, is_private=bool(is_private)))
        
    contents = await file.read()
    async with aiofiles.open(destination_path, 'wb') as f:
        await f.write(contents)
    
    return RedirectResponse('/', status_code=303)



@router.get('/download/{file_id}')
async def download(
    file_id: int,
    request: Request,
    current_user: CurrentUser, 
    session: SqliteSessionDep,
):  
    file = await session.get(File, file_id)
    
    if not file:
        set_flash_message(request, 'Error during file downloading')
        return RedirectResponse('/', status_code=303)
    
    if file.is_private and not current_user.is_superuser:
        set_flash_message(request, 'You have no permission')
        return RedirectResponse('/', status_code=303)
    
    file.downloads += 1
    session.add(file)
    
    current_user.downloads += 1
    session.add(current_user)
    
    await session.commit()
    
    logger.info(
        f'{current_user.name} downloaded file "{file.filename}" at {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
    )
    
    return FileResponse(
        path='src/static/files/' + file.filename,
        media_type='application/octet-stream',
        filename=file.filename
    )

    
@router.get('/delete/{file_id}')
async def delete(
    file_id: int,
    request: Request,
    current_user: CurrentSuperUser, 
    session: SqliteSessionDep,
):
    file = await session.get(File, file_id)
    if not file:
        set_flash_message(request, 'File does not exist')
        return RedirectResponse('/', status_code=303)
    await session.delete(file)
    await session.commit()
    
    if os.path.exists('src/static/files/'+file.filename):
        os.remove('src/static/files/'+file.filename)
    return RedirectResponse('/', status_code=303)



@router.get('/toggleprivacy/{file_id}')
async def toggleadmin(
    file_id: int,
    request: Request,
    current_user: CurrentSuperUser, 
    session: SqliteSessionDep,
):  
    file: File = await session.get(File, file_id)
    
    if not file:
        set_flash_message(request, 'File does not exist')
        return RedirectResponse('/', status_code=303)
    
    file.is_private = not file.is_private
    session.add(file)
    
    await session.commit()
    
    return RedirectResponse('/', status_code=303)

@router.get('/users/toggleadmin/{user_id}')
async def toggleadmin(
    user_id: int,
    request: Request,
    current_user: CurrentSuperUser, 
    session: SqliteSessionDep,
):  
    user: User = await session.get(User, user_id)
    
    if not user:
        set_flash_message(request, 'User does not exist')
        return RedirectResponse('/users', status_code=303)
    
    user.is_superuser = not user.is_superuser
    session.add(user)
    
    await session.commit()
    
    return RedirectResponse('/users', status_code=303)