from pydantic import BaseModel


class Pagination(BaseModel):
    page: int = 1
    size: int = 10
