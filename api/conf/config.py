from typing import Iterator, Generator, Annotated

from fastapi import Depends
from pydantic.v1 import BaseSettings
from sqlalchemy import create_engine
from sqlmodel import Session

from api.conf import root_path

# 读取常量配置
class Constant(BaseSettings):
    oss_bucket_name: str = "oss_bucket_name"
    oss_endpoint: str = "oss_endpoint"
    access_key_id: str = "oss_access_key_id"
    access_key_secret: str = "oss"
    db_host: str = "db_host"
    db_port: str = "db_port"
    db_user: str = "db_user"
    db_password: str = "db_password"
    db_name: str = "db_name"

    class Config:
        env_file = f"{root_path}/.env"
        env_file_encoding = "utf-8"
        # case_sensitive = True
        # env_prefix = "FASTAPI_"

constant = Constant()

def init_db():
    return create_engine(
        f"postgresql://{constant.db_user}:{constant.db_password}@{constant.db_host}:{constant.db_port}/{constant.db_name}?sslmode=require")

def get_db() -> Generator[Session, None, None]:
    with Session(init_db()) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_db)]

