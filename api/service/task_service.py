import asyncio
import json
from datetime import datetime

from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from api.client import dashscope_client, keling_client
from api.client.aliyun_client import AliyunClient
from api.model.task import TaskParams, Task, ImageToVideoParams
from api.model.user import User


async def task_processing(session: AsyncSession, task: Task, task_params: TaskParams):
    if task.task_type == 1:
        aliyun_client = AliyunClient()
        is_success, finish_url = await translate_image(aliyun_client, task_params.image_translate_params.origin_url,
                                                  task_params.image_translate_params.source_language,
                                                  task_params.image_translate_params.target_language,
                                                  task_params.image_translate_params.ignore_entity_recognize)
        task.finish_url = [finish_url]
        if not is_success:
            task.fail_msg = "图片翻译失败"
        logger.info(f"图片翻译{is_success}, finish_url: {finish_url}")
    elif task.task_type == 2:
        is_success, result_urls = await background_generation(task_params.background_generation_params.origin_url,
                                                          task_params.background_generation_params.ref_image_url,
                                                          task_params.background_generation_params.ref_prompt,
                                                          task_params.background_generation_params.foreground_edges,
                                                          task_params.background_generation_params.background_edges,
                                                          task_params.background_generation_params.foreground_edge_prompts,
                                                          task_params.background_generation_params.background_edge_prompts,
                                                          task_params.background_generation_params.n,
                                                          task_params.background_generation_params.ref_prompt_weight,
                                                          task_params.background_generation_params.model_version)
        task.finish_url = result_urls
        if not is_success:
            task.fail_msg = "背景生成失败"
        logger.info(f"背景生成{is_success}, finish_url: {result_urls}")
    elif task.task_type == 3:
        task.task_content = task_params.image_to_video_params.model_dump()
        is_success, result_urls = await image_to_video_service(task_params.image_to_video_params)
        task.finish_url = result_urls
        if not is_success:
            task.fail_msg = "图片生成视频失败"
    elif task.task_type == 4:
        aliyun_client = AliyunClient()
        is_success, finish_url = await segment_commodity(aliyun_client, task_params.image_segment_params.image_url)
        task.finish_url = [finish_url]
        if not is_success:
            task.fail_msg = "商品分割失败"
        logger.info(f"商品分割{is_success}, finish_url: {finish_url}")
    elif task.task_type == 100:
        task.finish_url = ["https:xxx.com"]
        is_success = True
        logger.info("测试命中")
    else:
        raise ValueError("未知任务类型")
    if is_success:
        task.task_status = 2
    task.finish_time = datetime.now()
    session.add(task)
    await session.commit()

# 图片翻译任务
async def translate_image(aliyun_client, url, source_language, target_language, ignore_entity_recognize):
    result = await aliyun_client.translate_image(url, source_language, target_language, ignore_entity_recognize)
    if result.status_code != 200:
        return False, result.data.message
    return True, result.body.data.final_image_url

# 抠图任务
async def segment_commodity(aliyun_client, url):
    result = await aliyun_client.segment_commodity(url)
    if result.status_code != 200:
        return False, result.data.message
    return True, result.body.data.final_image_url

# 图像背景生成
async def background_generation(base_image_url, ref_image_url, ref_prompt, foreground_edges, background_edges,
                         foreground_edge_prompts, background_edge_prompts, n, ref_prompt_weight, model_version):
    if base_image_url is None or (ref_image_url is None and ref_prompt is None):
         raise ValueError("base_image_url必填, ref_image_url, ref_prompt 必须选填一个")
    result = await dashscope_client.generate_background(base_image_url, ref_image_url, ref_prompt, foreground_edges,
                                 background_edges, foreground_edge_prompts, background_edge_prompts, n, ref_prompt_weight, model_version)
    task_id = result['output']['task_id']
    while True:
        await asyncio.sleep(2)
        result = await dashscope_client.get_task_result(task_id)
        status = result['output']['task_status']
        logger.info(f"背景生成结果查询: task_id: {task_id}, status: {status}")
        if status == 'SUCCEEDED':
            urls = [item['url'] for item in result['output']['results']]
            return True, urls
        elif status == 'FAILED':
            return False, result['output']['message']
        else:
            continue

# 图片转视频
async def image_to_video_service(param: ImageToVideoParams):
    if param.image is None and param.model_name is None:
        raise ValueError("image, model_name必填")
    task_create_resp = await keling_client.text2video_task(param.model_name, param.image,
                                  param.mode, param.duration, param.prompt, param.cfg_scale, param.static_mask,
                                  param.negative_prompt)
    if task_create_resp['code'] != 0 or task_create_resp['data']['task_id'] is None:
        return False, task_create_resp['msg']
    task_id = task_create_resp['data']['task_id']
    while True:
        await asyncio.sleep(30)
        result = await keling_client.text2video_result(task_id)
        status = result['data']['task_status']
        logger.info(f"图片生成视频结果查询: task_id: {task_id}, status: {status}")
        if status == 'succeed':
            urls = [result['data']['task_result']['videos'][0]['url']]
            return True, urls
        elif status == 'failed':
            return False, result['msg']
        else:
            continue
