import asyncio
import time

import httpx
import jwt
from loguru import logger

from api.conf.config import constant

BASE_URL = "https://api.klingai.com"

def encode_jwt_token():
    headers = {
        "alg": "HS256",
        "typ": "JWT"
    }
    payload = {
        "iss": constant.keling_access_key_id,
        "exp": int(time.time()) + 1800, # 有效时间，此处示例代表当前时间+1800s(30min)
        "nbf": int(time.time()) - 5 # 开始生效的时间，此处示例代表当前时间-5秒
    }
    token = jwt.encode(payload, constant.keling_access_key_secret, headers=headers)
    return token

def get_header():
    return {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + encode_jwt_token()
    }

# 创建任务
async def text2video_task(model_name, image,
    mode=None, duration=None, prompt=None, cfg_scale=None, static_mask=None, negative_prompt=None):
    data = {
        "model_name": model_name,
        "image": image,
    }
    if mode is not None:
        data["mode"] = mode
    if duration is not None:
        data["duration"] = duration
    if prompt is not None:
        data["prompt"] = prompt
    if cfg_scale is not None:
        data["cfg_scale"] = cfg_scale
    if static_mask is not None:
        data["static_mask"] = static_mask
    if negative_prompt is not None:
        data["negative_prompt"] = negative_prompt
    # if dynamic_masks is not None:
    #     data["dynamic_masks"] = dynamic_masks
    logger.info(f"text2video_task 创建任务参数: {data}")

    url = "/v1/videos/image2video"
    async with httpx.AsyncClient() as client:
        response = await client.post(
            url=BASE_URL + url,
            headers=get_header(),
            json=data
        )
        response.raise_for_status()
        return response.json()

# 查询任务结果
async def text2video_result(task_id):
    url = f"/v1/videos/image2video/{task_id}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url=BASE_URL + url,
                                    headers=get_header())
        response.raise_for_status()
        return response.json()

if __name__ == '__main__':
    data = {
    "model_name": "kling-v1",
    "mode": "pro",
    "duration": "5",
    "image": "https://h2.inkwai.com/bs2/upload-ylab-stunt/se/ai_portal_queue_mmu_image_upscale_aiweb/3214b798-e1b4-4b00-b7af-72b5b0417420_raw_image_0.jpg",
    "prompt": "宇航员站起身走了",
    "cfg_scale": "0.5",
    "static_mask": "https://h2.inkwai.com/bs2/upload-ylab-stunt/ai_portal/1732888177/cOLNrShrSO/static_mask.png",
    "dynamic_masks": [
      {
        "mask": "https://h2.inkwai.com/bs2/upload-ylab-stunt/ai_portal/1732888130/WU8spl23dA/dynamic_mask_1.png",
        "trajectories": [
          {"x":279,"y":219},{"x":417,"y":65}
        ]
      }
    ]
}
    # result = asyncio.run(text2video_task(data))
    result = asyncio.run(text2video_result("CjNTkGdSwxYAAAAAAE0JIA"))
    print(result)
