from pydantic import BaseModel
from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class User(SQLModel, table=True):
    __tablename__ = "j_user"
    __table_args__ = {"schema": "j_base"}

    id: Optional[int] = Field(default=None, primary_key=True, description="用户ID")
    email: str = Field(default="", max_length=128, description="email地址")
    status: int = Field(default=0, description="状态:0=正常,1=禁用")
    login_at: datetime = Field(default=datetime(1970, 1, 1, 8, 0, 0), description="登录时间")
    create_id: int = Field(default=0, description="创建者ID")
    create_name: str = Field(default="", max_length=56, description="创建者名称")
    create_at: datetime = Field(default_factory=datetime.utcnow, description="创建时间")
    update_id: str = Field(default="", max_length=56, description="更新者ID")
    update_name: str = Field(default="", max_length=56, description="更新者名称")
    update_at: datetime = Field(default_factory=datetime.utcnow, description="更新时间")
    delete: int = Field(default=0, description="是否删除:0=未删除,1=已删除")
    delete_at: datetime = Field(default=datetime(1970, 1, 1, 8, 0, 0), description="删除时间")

    class Config:
        from_attributes = True

class UserQuery(BaseModel):
    id: Optional[int] = None
    email: Optional[str] = None
    page: int = 1
    size: int = 10
    status: Optional[int] = None
    verification_code: Optional[str] = None

class CacheUser(BaseModel):
    id: int
    email: str
