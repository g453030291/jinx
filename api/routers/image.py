import uuid
from urllib.parse import urlparse

from controlnet_aux.processor import Processor
from fastapi import APIRouter, Body

from PIL import Image
import requests
from io import BytesIO
from api.client.oss_client import OSSClient
from api.model.resp import Resp

router = APIRouter()

# 生成一个图片处理的方法
@router.post("/foreground/generate", response_model=Resp)
def foreground_edges_generate(o_url: str = Body(..., embed=True)):
    pass
    # hed_processor = Processor('softedge_hed')
    # if o_url.startswith("https://tristana-oss.oss-cn-shanghai.aliyuncs.com"):
    #     oss_client = OSSClient()
    #     img_data = oss_client.get_object(urlparse(o_url).path[1:])
    # else:
    #     response = requests.get(o_url)
    #     response.raise_for_status()
    #     img_data = response.content
    # img = Image.open(BytesIO(img_data))
    # if img.mode == 'RGBA':
    #     r, g, b, a = img.split()
    #     img = img.convert('RGB')
    #     hed_img = hed_processor(img, to_pil=True).resize(img.size).convert('RGB')
    #     hed_img.putalpha(a)
    # else:
    #     img = img.convert('RGB')
    #     hed_img = hed_processor(img, to_pil=True).resize(img.size).convert('RGB')
    #
    # oss_client = OSSClient()
    # output = BytesIO()
    # hed_img.save(output, format='PNG')
    # output.seek(0)
    # oss_url = oss_client.put_object(str(uuid.uuid4()).replace('-', '') + '.png', output.read())
    #
    # return Resp.success(data=oss_url)
