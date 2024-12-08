from typing import Any

from fastapi import APIRouter, HTTPException, Body, BackgroundTasks, Depends
from fastapi_pagination import Params
from fastapi_pagination.ext.sqlalchemy import paginate
from loguru import logger
from sqlalchemy.future import select

from api.conf.config import SessionDep
from api.model.resp import Resp
from api.model.task import Task, TaskQuery, TaskParams
from api.model.user import User
from api.service import task_service
from api.service.auth_service import get_current_user

router = APIRouter(prefix="/task")

@router.post("/create", response_model=Resp)
async def create_task(background_tasks: BackgroundTasks,
                session: SessionDep,
                task_params: TaskParams,
                current_user: User = Depends(get_current_user)) -> Any:
    try:
        task_params_dict = task_params.model_dump()
        task = Task(**task_params_dict)
        task.task_status = 3
        task.create_id = current_user.id
        if task.task_type == 1:
            task.task_content = task_params.image_translate_params.model_dump()
        elif task.task_type == 2:
            task.task_content = task_params.background_generation_params.model_dump()
        elif task.task_type == 3:
            task.task_content = task_params.image_to_video_params.model_dump()

        session.add(task)
        await session.commit()
        await session.refresh(task)
        logger.info(f"task create success, task_id: {task.id}")
        background_tasks.add_task(task_service.task_processing, session, task, task_params)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return Resp.success('task processing')

@router.post("/list", response_model=Resp)
async def list_tasks(session: SessionDep, taskQuery: TaskQuery = Body(...)) -> Any:
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
    page_result = await paginate(session, query, params=page_params)
    return Resp.success(data=page_result)

@router.post("/delete", response_model=Resp)
async def delete_task(session: SessionDep, id: int = Body(..., embed=True)) -> Any:
    try:
        statement = select(Task).where(Task.id == id)
        result = session.execute(statement).scalars().first()
        if not result:
            raise HTTPException(status_code=404, detail="Task not found")
        result.delete = 1
        session.add(result)
        await session.commit()
        await session.refresh(result)
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    return Resp.success(True)

@router.get("/{id}", response_model=Resp)
async def get_task(session: SessionDep, id: int) -> Any:
    statement = select(Task).where(Task.id == id)
    result = (await session.execute(statement)).scalars().first()
    if not result:
        raise HTTPException(status_code=404, detail="Task not found")
    return Resp.success(data=result)
