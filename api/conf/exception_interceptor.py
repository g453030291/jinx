from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from api.model.resp import Resp

class ExceptionInterceptor:
    @staticmethod
    async def http_exception_handler(request: Request, exc: HTTPException):
        resp = Resp.fail(msg=exc.detail, code=exc.status_code)
        return JSONResponse(
            status_code=exc.status_code,
            content=resp.model_dump(),
        )

    @staticmethod
    async def general_exception_handler(request: Request, exc: Exception):
        resp = Resp.fail(msg=str(exc), code=500)
        return JSONResponse(
            status_code=500,
            content=resp.model_dump(),
        )