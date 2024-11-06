from typing import Any

from fastapi import APIRouter, HTTPException, Body
from fastapi_pagination import Page, Params
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.future import select

from api.client.aliyun_client import AliyunClient
from api.conf.config import SessionDep
from api.model import resp
from api.model.resp import Resp
from api.model.task import Task, TaskQuery
from api.service import task_service

router = APIRouter()

@router.post("/task/create", response_model=Task)
def create_task(session: SessionDep, task: Task) -> Any:
    try:
        aliyun_client = AliyunClient()
        is_success, finish_url = task_service.translate_image(aliyun_client, task.origin_url, task.source_language, task.target_language)
        if not is_success:
            task.task_status = 3
            task.fail_msg = "图片翻译失败"
        else:
            task.task_status = 2
            task.finish_url = finish_url
        session.add(task)
        session.commit()
        session.refresh(task)
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    return Resp.success(task)

@router.post("/task/list", response_model=Resp)
def list_tasks(session: SessionDep, taskQuery: TaskQuery = Body(...)) -> Any:
    filters = []
    filters.append(Task.delete == 0)
    if taskQuery.id:
        filters.append(Task.id == taskQuery.id)
    if taskQuery.task_type:
        filters.append(Task.task_type == taskQuery.task_type)
    if taskQuery.task_status:
        filters.append(Task.task_status == taskQuery.task_status)
    if taskQuery.task_name:
        filters.append(Task.task_name.ilike(f"%{taskQuery.task_name}%"))
    if taskQuery.create_id:
        filters.append(Task.create_id == taskQuery.create_id)

    query = select(Task).where(*filters) if filters else select(Task)
    page_params = Params(page=taskQuery.page, size=taskQuery.size)
    page_result = paginate(session, query, params=page_params)
    return Resp.success(data=page_result)

@router.post("/task/delete", response_model=Task)
def delete_task(session: SessionDep, id: int = Body(..., embed=True)) -> Any:
    try:
        statement = select(Task).where(Task.id == id)
        result = session.execute(statement).scalars().first()
        if not result:
            raise HTTPException(status_code=404, detail="Task not found")
        result.delete = 1
        session.add(result)
        session.commit()
        session.refresh(result)
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    return Resp.success(True)
