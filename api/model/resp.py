from pydantic.v1 import BaseModel
from typing import Any, Dict, Union

class Resp(BaseModel):
    code: int
    msg: str
    data: Union[Dict[str, Any], None]  # data 可以是字典或 None

    @classmethod
    def success(cls, msg: str = "Success", data: Union[Dict[str, Any], None] = None) -> "Resp":
        return cls(code=200, msg=msg, data=data)

    @classmethod
    def fail(cls, msg: str = "Failure", code: int = 400, data: Union[Dict[str, Any], None] = None) -> "Resp":
        return cls(code=code, msg=msg, data=data)
