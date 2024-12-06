import json
from datetime import datetime

from sqlmodel import update, select

import jwt
from fastapi import APIRouter, Body

from api.conf import config
from api.conf.config import SessionDep
from api.model.resp import Resp
from api.model.user import UserQuery, User, CacheUser
from api.util import str_util
from api.util.brevo_util import BrevoUtil

router = APIRouter()

# 发送验证码
@router.post("/send_code", response_model=Resp)
def send_code(userQuery: UserQuery = Body(...)):
    ver_code = str_util.generate_random_code()
    brevo_util = BrevoUtil()
    brevo_util.send_verification_email(userQuery.email, ver_code)
    config.redis.set(ver_code, userQuery.email, ex=60)
    return Resp.success('The verification code has been sent to your email, please check.')

# 登录
@router.post("/login", response_model=Resp)
async def login_or_register(session: SessionDep, userQuery: UserQuery = Body(...)):
    email = config.redis.get(userQuery.verification_code)
    if not email:
        return Resp.fail("Verification code error")
    statement = select(User).where(User.email == email)
    result = await session.execute(statement)
    login_user = result.scalars().first()
    if login_user:
        await session.execute(update(User).where(User.id == login_user.id).values(login_at=datetime.now()))
    else:
        login_user = User(email=email, login_at=datetime.now())
        session.add(login_user)
        await session.commit()
        await session.refresh(login_user)

    db_user = await session.execute(select(User).where(User.id == login_user.id))
    db_user = db_user.scalars().first()
    cache_user = CacheUser(**db_user.dict())
    token = jwt.encode(cache_user, 'jinxtestp', algorithm='HS256')
    config.redis.set(token, json.dumps(cache_user), ex=60 * 60 * 24 * 14)
    return Resp.success(data={"token": token})
