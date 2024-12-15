import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Depends
from fastapi_pagination import add_pagination
from loguru import logger
from fastapi.middleware.cors import CORSMiddleware

from api.conf import config
from api.conf.exception_interceptor import ExceptionInterceptor
from api.crawler import youtube
from api.routers import file_router, base, task_router, image_router, user_router, login_router, audio_router, \
    llm_router, enum_router
from api.service.auth_service import get_current_user

API_END_POINTS = '/api'

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info('on_startup')
    try:
        yield
    finally:
        logger.info('on_shutdown')
        await config.engine.dispose()

app = FastAPI(docs_url="/api/py/docs", openapi_url="/api/py/openapi.json", lifespan=lifespan)

config.IS_PROD = os.getenv('ENVIRONMENT') == 'prod'
logger.info(f'is_prod: {config.IS_PROD}')

add_pagination(app)
app.add_exception_handler(HTTPException, ExceptionInterceptor.http_exception_handler)
app.add_exception_handler(Exception, ExceptionInterceptor.general_exception_handler)
origins = [
    "https://www.jinx-aa.xyz",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(base.router, prefix='')
app.include_router(login_router.router, prefix=API_END_POINTS)
app.include_router(file_router.router, prefix=API_END_POINTS, dependencies=[Depends(get_current_user)])
app.include_router(task_router.router, prefix=API_END_POINTS, dependencies=[Depends(get_current_user)])
app.include_router(image_router.router, prefix=API_END_POINTS, dependencies=[Depends(get_current_user)])
app.include_router(youtube.router, prefix=API_END_POINTS, dependencies=[Depends(get_current_user)])
app.include_router(user_router.router, prefix=API_END_POINTS, dependencies=[Depends(get_current_user)])
app.include_router(audio_router.router, prefix=API_END_POINTS, dependencies=[Depends(get_current_user)])
app.include_router(llm_router.router, prefix=API_END_POINTS, dependencies=[Depends(get_current_user)])
app.include_router(enum_router.router, prefix=API_END_POINTS, dependencies=[Depends(get_current_user)])