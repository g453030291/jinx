from sqlmodel import SQLModel, Field, create_engine, Session, select
from typing import Optional
from datetime import datetime

from api.conf.config import constant
from api.model.page import Pagination


class Task(SQLModel, table=True):
    __tablename__ = "task"
    __table_args__ = {"schema": "j_base"}

    id: Optional[int] = Field(default=None, primary_key=True, description="任务ID")
    task_type: int = Field(default=0, description="任务类型:1=图片翻译")
    task_status: int = Field(default=0, description="任务状态:0=初始化,1=执行中, 2=成功,3=失败")
    fail_msg: str = Field(default="", max_length=256, description="任务失败原因")
    task_name: str = Field(default="", max_length=56, description="任务名称")
    origin_url: str = Field(default="", max_length=512, description="原始URL")
    source_language: str = Field(default="", max_length=56, description="源语言")
    target_language: str = Field(default="", max_length=56, description="目标语言")
    finish_url: str = Field(default="", max_length=512, description="完成URL")
    finish_time: datetime = Field(default=datetime(1970, 1, 1, 8, 0, 0), description="完成时间")
    create_id: int = Field(default=0, description="创建者ID")
    create_name: Optional[str] = Field(default="", max_length=56, description="创建者名称")
    create_at: datetime = Field(default_factory=datetime.utcnow, description="创建时间")
    update_at: datetime = Field(default_factory=datetime.utcnow, description="更新时间")
    update_id: int = Field(default=0, description="更新者ID")
    update_name: Optional[str] = Field(default="", max_length=56, description="更新者名称")
    delete_at: datetime = Field(default=datetime(1970, 1, 1, 8, 0, 0), description="删除时间")
    delete: int = Field(default=0, description="是否删除:0=未删除,1=已删除")

    class Config:
        from_attributes = True

class TaskQuery(Pagination):
    id: int = Field(default=None, description="任务ID")
    task_type: int = Field(default=0, description="任务类型:1=图片翻译")
    task_status: int = Field(default=0, description="任务状态:0=初始化,1=执行中, 2=成功,3=失败")
    task_name: str = Field(default="", description="任务名称")
    create_id: int = Field(default=0, description="创建者ID")



if __name__ == '__main__':
    engine = create_engine(f"postgresql://{constant.db_user}:{constant.db_password}@{constant.db_host}:{constant.db_port}/{constant.db_name}?sslmode=require")

    with Session(engine) as session:
        statement = select(Task).where(Task.id == 1)
        task = session.exec(statement).first()

        print(task)
