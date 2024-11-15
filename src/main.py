from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from .core.config import settings
from . import pages
from .initial_data import init


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init()
    yield


app = FastAPI(title='Test Task Full Stack Developer (Web, Python)', lifespan=lifespan)

app.mount('/static', StaticFiles(directory='src/static'), name="static")

app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)

# app.include_router(api.api_router, prefix='/api')
app.include_router(pages.router, prefix='')