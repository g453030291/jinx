import asyncio

from loguru import logger
from requests import request

from api.conf.config import constant

import httpx

# aliyun 百炼大模型

URL = 'https://dashscope.aliyuncs.com/api/v1/services/aigc/background-generation/generation/'
HEADERS = {
    'X-DashScope-Async': 'enable',
    'Authorization': f'Bearer {constant.ali_bai_lian_api_key}',
    'Content-Type': 'application/json'
}

# 生成背景
# base_image_url必传,
# ref_image_url, ref_prompt必传一个
async def generate_background(
    base_image_url,
    ref_image_url=None,
    ref_prompt=None,
    foreground_edges=None,
    background_edges=None,
    foreground_edge_prompt=None,
    background_edge_prompt=None,
    n=None,
    ref_prompt_weight=None,
    model_version=None
):
    data = {
        "model": "wanx-background-generation-v2",
        "input": {
            "base_image_url": base_image_url,
            "reference_edge": {}
        }
    }
    # 添加可选的 input 参数
    if ref_image_url:
        data["input"]["ref_image_url"] = ref_image_url
    if ref_prompt:
        data["input"]["ref_prompt"] = ref_prompt
    if foreground_edges:
        data["input"]["reference_edge"]["foreground_edge"] = foreground_edges
    if background_edges:
        data["input"]["reference_edge"]["background_edge"] = background_edges
    if foreground_edge_prompt:
        data["input"]["reference_edge"]["foreground_edge_prompt"] = foreground_edge_prompt
    if background_edge_prompt:
        data["input"]["reference_edge"]["background_edge_prompt"] = background_edge_prompt

    # 构建可选的 parameters 参数
    parameters = {}
    if n is not None:
        parameters["n"] = n
    if ref_prompt_weight:
        parameters["ref_prompt_weight"] = ref_prompt_weight
    if model_version:
        parameters["model_version"] = model_version
    if parameters:
        data["parameters"] = parameters
    logger.info(data)
    async with httpx.AsyncClient() as client:
        response = await client.post(URL, headers=HEADERS, json=data)
        logger.info(response.text)
        response.raise_for_status()
        return response.json()

# 查询任务结果
# GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}
async def get_task_result(task_id):
    url = f'https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}'
    headers = {
        'Authorization': f'Bearer {constant.ali_bai_lian_api_key}'
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        response.raise_for_status()  # 检查请求是否成功
        return response.json()

# Example usage:
base_image_url = 'https://vision-poster.oss-cn-shanghai.aliyuncs.com/lllcho.lc/data/test_data/images/main_images/new_main_img/a.png'
ref_image_url = 'http://vision-poster.oss-cn-shanghai.aliyuncs.com/lllcho.lc/data/test_data/images/ref_images/c5e50d27be534709817b2ab080b0162f_0.jpg'
ref_prompt = '山脉和晚霞'
foreground_edges = [
    'https://vision-poster.oss-cn-shanghai.aliyuncs.com/lllcho.lc/data/test_data/images/huaban_soft_edge/6cdd13941cef1b11d885aea1717b983ae566b8efc9094-vcsvxa_fw658webp.png',
    'http://vision-poster.oss-cn-shanghai.aliyuncs.com/lllcho.lc/data/test_data/images/ref_edge/2c36cc4b7da027279e87311dac48fc2d5d784b1e72c0e-x4f1wC_fw658webp.png'
]
background_edges = [
    'http://vision-poster.oss-cn-shanghai.aliyuncs.com/lllcho.lc/data/test_data/images/ref_edge/0718a9741e07c52ca5506e75c4f2b99e22fff68a4c7d3-P9WGLr_fw658webp.png'
]
foreground_edge_prompts = None
background_edge_prompts = None

async def main_test():
    # response = await generate_background(base_image_url=base_image_url, ref_image_url=ref_image_url, ref_prompt=None)
    # print(response)
    result = await get_task_result('72dc6194-ad6d-4e09-88b7-6fbca538ba86')
    print(result)

if __name__ == '__main__':
    data = {
        "model": "wanx-background-generation-v2",
        "input": {
            "base_image_url":
                "http://vibktprfx-prod-prod-damo-eas-cn-shanghai.oss-cn-shanghai.aliyuncs.com/seg-common-image/2025-01-12/9e503b79-6164-4f14-95b7-7438126af458/image.png?Expires=1736667780&OSSAccessKeyId=LTAI4FoLmvQ9urWXgSRpDvh1&Signature=0uRSwx2uMf%2BtynV73Oo9QzmNQFw%3D"
            ,
            "ref_prompt": "创建一个适合淘宝橱窗展示商品图的自然场景风格背景：要有柔和的阳光洒下，画面主体是一片长满各种鲜花（如雏菊、郁金香等）的草地，远处有葱郁的树林，天空中飘着几朵洁白的云朵，草地上可以有一些晶莹的露珠，整体色彩鲜艳、明亮且和谐，以突出商品的展示效果。"
        },
        "parameters": {
            "n": 3,
            "ref_prompt_weight": 0.5,
            "model_version": "v3"
        }
    }
    result = request('POST', url=URL, json=data, headers=HEADERS)
    print(result.text)
    # asyncio.run(main_test())
    # task_id = response['output']['task_id']
    # result = get_task_result('99c7a783-19f7-4816-8b4a-4434df34286c')
    # print(result)
