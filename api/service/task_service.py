import asyncio
import json
from datetime import datetime

from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from api.client import dashscope_client
from api.client.aliyun_client import AliyunClient
from api.model.task import TaskParams, Task

async def task_processing(session: AsyncSession, task_params: TaskParams):
    task_params_dict = task_params.model_dump()
    task = Task(**task_params_dict)
    task.task_status = 3
    if task.task_type == 1:
        task.task_content = task_params.image_translate_params.model_dump()
        aliyun_client = AliyunClient()
        is_success, finish_url =  translate_image(aliyun_client, task_params.image_translate_params.origin_url, task_params.image_translate_params.source_language, task_params.image_translate_params.target_language)
        task.finish_url = [finish_url]
        if not is_success:
            task.fail_msg = "图片翻译失败"
        logger.info(f"图片翻译{is_success}, finish_url: {finish_url}")
    elif task.task_type == 2:
        task.task_content = task_params.background_generation_params.model_dump()
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
    else:
        raise ValueError("未知任务类型")
    if is_success:
        task.task_status = 2
    task.finish_time = datetime.now()
    session.add(task)
    await session.commit()

# 图片翻译任务
def translate_image(aliyun_client, url, source_language, target_language):
    result = aliyun_client.translate_image(url, source_language, target_language)
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
