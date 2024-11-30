from typing import Any

from fastapi import APIRouter, HTTPException, Body
from fastapi_pagination import Params
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.future import select

from api.conf.config import SessionDep
from api.model.resp import Resp
from api.model.user import User, UserQuery

router = APIRouter()

@router.post("/user/list", response_model=Resp)
async def list_users(session: SessionDep, userQuery: UserQuery = Body(...)) -> Any:
    filters = []
    filters.append(User.delete == 0)
    if userQuery.id:
        filters.append(User.id == userQuery.id)
    if userQuery.email:
        filters.append(User.email.ilike(f"%{userQuery.email}%"))
    if userQuery.status:
        filters.append(User.status == userQuery.status)

    query = select(User).where(*filters) if filters else select(User)
    page_params = Params(page=userQuery.page, size=userQuery.size)
    page_result = await paginate(session, query, params=page_params)
    return Resp.success(data=page_result)
