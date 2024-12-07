from fastapi import APIRouter, Body

from api.model.completion import CompletionParams
from api.model.resp import Resp
from api.service import llm_service

router = APIRouter(prefix="/llm")

@router.post("/completions", response_model=Resp)
def completions(params: CompletionParams = Body(...)) -> Resp:
    result = llm_service.completions(system_prompts=params.system_prompts, user_prompts=params.user_prompts,
                                     image_list=params.image_list)
    return Resp.success(data=result)
