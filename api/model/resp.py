from pydantic import BaseModel
from typing import Any, Dict, Union, Optional


class Resp(BaseModel):
    code: int
    msg: str
    data: Optional[Any] = None

    @classmethod
    def success(cls, data: Optional[Any] = None) -> "Resp":
        return cls(code=200, msg="success", data=data)

    @classmethod
    def fail(cls, msg: str = "failure", code: int = 400, data: Union[Dict[str, Any], None] = None) -> "Resp":
        return cls(code=code, msg=msg, data=data)
