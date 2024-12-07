from typing import Any

from fastapi import APIRouter, HTTPException, Body, BackgroundTasks, Depends
from fastapi_pagination import Params
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.future import select

from api.conf.config import SessionDep
from api.model.resp import Resp
from api.model.task import Task, TaskQuery, TaskParams
from api.model.user import User
from api.service import task_service
from api.service.auth_service import get_current_user

router = APIRouter()

@router.post("/task/create", response_model=Resp)
def create_task(background_tasks: BackgroundTasks,
                session: SessionDep,
                task_params: TaskParams,
                current_user: User = Depends(get_current_user)) -> Any:
    try:
        background_tasks.add_task(task_service.task_processing, session, current_user, task_params)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return Resp.success('task processing')

@router.post("/task/list", response_model=Resp)
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

@router.post("/task/delete", response_model=Resp)
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
