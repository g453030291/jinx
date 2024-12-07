from fastapi import APIRouter

from api.model.resp import Resp

router = APIRouter(prefix="/enum")

@router.get("/translate/language", response_model=Resp)
def target_language(language: str):
    result_map = []
    if language == 'zh':
        result_map = [
            {"name": "English", "value": "en"},
            {"name": "Russian", "value": "ru"},
            {"name": "Spanish", "value": "es"},
            {"name": "French", "value": "fr"},
            {"name": "German", "value": "de"},
            {"name": "Italian", "value": "it"},
            {"name": "Dutch", "value": "nl"},
            {"name": "Portuguese", "value": "pt"},
            {"name": "Vietnamese", "value": "vi"},
            {"name": "Turkish", "value": "tr"},
            {"name": "Malay", "value": "ms"},
            {"name": "Thai", "value": "th"},
            {"name": "Polish", "value": "pl"},
            {"name": "Japanese", "value": "ja"},
            {"name": "Korean", "value": "ko"}
        ]
    if language == 'en':
        result_map = [
            {"name": "Chinese", "value": "zh"},
            {"name": "Russian", "value": "ru"},
            {"name": "Spanish", "value": "es"},
            {"name": "French", "value": "fr"},
            {"name": "German", "value": "de"},
            {"name": "Italian", "value": "it"},
            {"name": "Dutch", "value": "nl"},
            {"name": "Portuguese", "value": "pt"},
            {"name": "Vietnamese", "value": "vi"},
            {"name": "Turkish", "value": "tr"},
            {"name": "Malay", "value": "ms"},
            {"name": "Thai", "value": "th"},
            {"name": "Polish", "value": "pl"},
            {"name": "Japanese", "value": "ja"},
            {"name": "Korean", "value": "ko"}
        ]
    return Resp.success(data=result_map)
