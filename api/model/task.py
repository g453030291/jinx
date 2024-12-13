from pydantic import BaseModel
from sqlalchemy import false, Column, JSON
from sqlmodel import SQLModel, Field, create_engine, Session, select
from typing import Optional, List
from datetime import datetime

from api.conf.config import constant
from api.model.page import Pagination


class Task(SQLModel, table=True):
    __tablename__ = "task"
    __table_args__ = {"schema": "j_base"}

    id: Optional[int] = Field(default=None, primary_key=True, description="任务ID")
    task_type: int = Field(default=0, description="任务类型:1=图片翻译,2=背景生成,3=图生视频")
    task_status: int = Field(default=0, description="任务状态:0=初始化,1=执行中, 2=成功,3=失败")
    fail_msg: str = Field(default="", max_length=256, description="任务失败原因")
    task_name: str = Field(default="", max_length=56, description="任务名称")
    finish_url: Optional[dict] = Field(default=None, sa_column=Column(JSON), description="完成URL")
    finish_time: datetime = Field(default=datetime(1970, 1, 1, 8, 0, 1), description="完成时间")
    task_content: Optional[dict] = Field(default=None, sa_column=Column(JSON), description="任务内容")
    create_id: int = Field(default=0, description="创建者ID")
    create_name: Optional[str] = Field(default="", max_length=56, description="创建者名称")
    create_at: datetime = Field(default_factory=datetime.utcnow, description="创建时间")
    update_at: datetime = Field(default_factory=datetime.utcnow, description="更新时间")
    update_id: int = Field(default=0, description="更新者ID")
    update_name: Optional[str] = Field(default="", max_length=56, description="更新者名称")
    delete_at: datetime = Field(default=datetime(1970, 1, 1, 8, 0, 1), description="删除时间")
    delete: int = Field(default=0, description="是否删除:0=未删除,1=已删除")

    class Config:
        from_attributes = True

class TaskQuery(Pagination):
    id: int = Field(default=None, description="任务ID")
    task_type: int = Field(default=0, description="任务类型:1=图片翻译,2=背景生成,3=图生视频")
    task_status: int = Field(default=0, description="任务状态:0=初始化,1=执行中, 2=成功,3=失败")
    task_name: str = Field(default="", description="任务名称")
    create_id: int = Field(default=0, description="创建者ID")


class ImageTranslateParams(BaseModel):
    origin_url: str = Field(default="", max_length=512, description="原始URL")
    source_language: str = Field(default="", max_length=56, description="源语言")
    target_language: str = Field(default="", max_length=56, description="目标语言")
    ignore_entity_recognize: Optional[bool] = Field(default=False, description="是否忽略实体识别")

class BackgroundGenerationParams(BaseModel):
    origin_url: str = Field(default="", max_length=512, description="基础图片URL")
    ref_image_url: Optional[str] = Field(default=None, max_length=512, description="参考图片URL")
    ref_prompt: Optional[str] = Field(default=None, max_length=256, description="参考提示")
    foreground_edges: Optional[List[str]] = Field(default=None, description="前景边缘")
    background_edges: Optional[List[str]] = Field(default=None, description="背景边缘")
    foreground_edge_prompts: Optional[List[str]] = Field(default=None, description="前景边缘提示")
    background_edge_prompts: Optional[List[str]] = Field(default=None, description="背景边缘提示")
    n: Optional[int] = Field(default=None, description="数量")
    ref_prompt_weight: Optional[float] = Field(default=None, description="参考提示权重")
    model_version: Optional[str] = Field(default=None, max_length=56, description="模型版本")

    class Config:
        protected_namespaces = ()

class ImageToVideoParams(BaseModel):
    model_name: str = Field(default="", description="模型名称:kling-v1, kling-v1-5")
    image: str = Field(default="", description="图片URL")
    mode: str = Field(default="", description="生成视频的模式:std，pro")
    # image_tail: str = Field(default="", max_length=512, description="参考图像(尾帧控制)url")
    prompt: str = Field(default="", description="正向提示词")
    negative_prompt: str = Field(default="", description="负向提示词")
    cfg_scale: float = Field(default="", description="生成视频的自由度")
    static_mask: str = Field(default="", description="静态遮罩图 url")
    # dynamic_masks: Optional[List[dict]] = Field(default=None, description="动态遮罩")
    duration: int = Field(default="", description="时长[5，10]")

    class Config:
        protected_namespaces = ()

class TaskParams(BaseModel):
    task_type: int = Field(default=0, description="任务类型:1=图片翻译,2=背景生成,3=图生视频")
    task_name: str = Field(default="", max_length=56, description="任务名称")
    image_translate_params: Optional[ImageTranslateParams] = Field(default=None, description="图片翻译参数")
    background_generation_params: Optional[BackgroundGenerationParams] = Field(default=None, description="背景生成参数")
    image_to_video_params: Optional[ImageToVideoParams] = Field(default=None, description="图片生成视频参数")




if __name__ == '__main__':
    engine = create_engine(f"postgresql://{constant.db_user}:{constant.db_password}@{constant.db_host}:{constant.db_port}/{constant.db_name}?sslmode=require")

    with Session(engine) as session:
        statement = select(Task).where(Task.id == 1)
        task = session.exec(statement).first()

        print(task)
