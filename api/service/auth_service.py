import json

from fastapi import Request, HTTPException

from api.conf.config import redis
from api.model.user import CacheUser

# 获取缓存的登录用户信息
async def get_current_user(request: Request):
    token = request.headers.get("Authorization")
    if not token:
        raise HTTPException(status_code=401, detail="Authorization header missing")

    cache_user_json = redis.get(token)
    if cache_user_json is None:
        raise HTTPException(status_code=401, detail="Invalid token")

    cache_user_dict = json.loads(cache_user_json)
    return CacheUser(**cache_user_dict)
