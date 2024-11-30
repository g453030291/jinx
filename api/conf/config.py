import os
import ssl
from typing import Annotated, AsyncGenerator

from fastapi import Depends
from pydantic.v1 import BaseSettings
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from api.conf import root_path

IS_PROD = os.getenv('ENV') == 'prod'

# 读取常量配置
class Constant(BaseSettings):
    oss_bucket_name: str = "oss_bucket_name"
    oss_endpoint: str = "oss_endpoint"
    access_key_id: str = "oss_access_key_id"
    access_key_secret: str = "oss"
    ali_bai_lian_api_key: str = "ali_bai_lian_api_key"
    db_host: str = "db_host"
    db_port: str = "db_port"
    db_user: str = "db_user"
    db_password: str = "db_password"
    db_name: str = "db_name"
    brevo_api_key: str = "brevo_api_key"

    class Config:
        if IS_PROD:
            env_file = None
        else:
            env_file = f"{root_path}/.env"
            env_file_encoding = "utf-8"
        # case_sensitive = True
        # env_prefix = "FASTAPI_"

constant = Constant()


# 创建 SSL 上下文
# ssl_context = ssl.create_default_context()

# 如果不需要验证 SSL 证书（不推荐在生产环境使用）
# ssl_context.check_hostname = False
# ssl_context.verify_mode = ssl.CERT_NONE

# 创建异步引擎
engine = create_async_engine(
    f"postgresql+asyncpg://{constant.db_user}:{constant.db_password}@{constant.db_host}:{constant.db_port}/{constant.db_name}",
    # connect_args={"ssl": ssl_context}
)

# 创建异步会话工厂
async_session_maker = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# 定义 get_db 函数，用于依赖注入
async def get_db():
    async with async_session_maker() as session:
        yield session

SessionDep = Annotated[AsyncSession, Depends(get_db)]

