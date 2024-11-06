from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi_pagination import add_pagination

from api.conf import config
from api.routes import file, base, task

API_END_POINTS = '/api'

@asynccontextmanager
async def lifespan(app: FastAPI):
    print('on_startup')
    config.init_db()
    print('db engine created')
    try:
        yield
    finally:
        print('on_shutdown')
        config.init_db().dispose()

app = FastAPI(docs_url="/api/py/docs", openapi_url="/api/py/openapi.json", lifespan=lifespan)
add_pagination(app)

app.include_router(base.router, prefix='')

app.include_router(file.router, prefix=API_END_POINTS)

app.include_router(task.router, prefix=API_END_POINTS)
