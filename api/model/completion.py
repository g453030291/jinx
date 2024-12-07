from typing import Optional, List

from pydantic import BaseModel

# llm请求参数
class CompletionParams(BaseModel):
    system_prompts: str = ""
    user_prompts: str
    image_list: Optional[List] = []
