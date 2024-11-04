from typing import Any

from fastapi import APIRouter, HTTPException, Depends, Body
from fastapi_pagination import Page, Params
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from api.conf.config import get_db
from api.model.task import Task, TaskQuery

router = APIRouter()

@router.post("/task/create", response_model=Task)
def create_task(task: Task, db: Session = Depends(get_db)) -> Any:
    try:
        db.add(task)
        db.commit()
        db.refresh(task)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    return task

@router.post("/task/list", response_model=Page[Task])
def list_tasks(taskQuery: TaskQuery = Body(...), db: Session = Depends(get_db)) -> Any:
    filters = []
    if taskQuery.id:
        filters.append(Task.id == taskQuery.id)
    if taskQuery.task_type:
        filters.append(Task.task_type == taskQuery.task_type)
    if taskQuery.task_status:
        filters.append(Task.task_status == taskQuery.task_status)
    if taskQuery.task_name:
        filters.append(Task.task_name.ilike(f"%{taskQuery.task_name}%"))
    if taskQuery.creator_id:
        filters.append(Task.creator_id == taskQuery.creator_id)

    query = select(Task).where(*filters) if filters else select(Task)
    page_params = Params(page=taskQuery.page, size=taskQuery.size)
    return paginate(db, query, params=page_params)

@router.post("/task/delete", response_model=Task)
def delete_task(task: Task, db: Session = Depends(get_db)) -> Any:
    try:
        statement = select(Task).where(Task.id == task.id)
        result = db.execute(statement).scalars().first()
        if not result:
            raise HTTPException(status_code=404, detail="Task not found")
        result.deleted = True
        db.add(result)
        db.commit()
        db.refresh(result)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    return result
