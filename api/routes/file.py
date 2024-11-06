from fastapi import FastAPI, UploadFile, File, APIRouter

from api.client.oss_client import OSSClient
from api.conf.config import Constant
from api.model.resp import Resp

router = APIRouter()

@router.post("/file/upload")
async def upload(files: list[UploadFile] = File(...)):
    urls = []
    oss_client = OSSClient()
    for file in files:
        contents = await file.read()
        filename = file.filename
        oss_client.put_object(filename, contents)
        urls.append(oss_client.get_object_url(filename))
    return Resp.success(data={"urls": urls})
