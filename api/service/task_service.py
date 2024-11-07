import time

from fastapi import HTTPException

from api.client import dashscope_client
from api.client.aliyun_client import AliyunClient


def add_task(session, task):
    task.task_status = 3
    if task.task_type == 1:
        aliyun_client = AliyunClient()
        is_success, finish_url = translate_image(aliyun_client, task.origin_url, task.source_language, task.target_language)
        task.finish_url = finish_url
        task.fail_msg = "图片翻译失败"
    elif task.task_type == 2:
        is_success, results = background_generation(task.origin_url, task.ref_image_url, task.ref_prompt, task.foreground_edges,
                                        task.background_edges, task.foreground_edge_prompts, task.background_edge_prompts)
        task.finish_url = ','.join(results)
        task.fail_msg = "背景生成失败"
    else:
        raise ValueError("未知任务类型")
    if is_success:
        task.task_status = 2
    session.add(task)
    session.commit()

# 图片翻译任务
def translate_image(aliyun_client, url, source_language, target_language):
    result = aliyun_client.translate_image(url, source_language, target_language)
    if result.status_code != 200:
        return False, result.data.message
    return True, result.body.data.final_image_url

# 图像背景生成
def background_generation(base_image_url, ref_image_url, ref_prompt, foreground_edges, background_edges,
                         foreground_edge_prompts, background_edge_prompts):
    if base_image_url is None or (ref_image_url is None and ref_prompt is None):
         raise ValueError("base_image_url必填, ref_image_url, ref_prompt 必须选填一个")
    result = dashscope_client.generate_background(base_image_url, ref_image_url, ref_prompt, foreground_edges,
                                 background_edges, foreground_edge_prompts, background_edge_prompts)
    task_id = result['output']['task_id']
    while True:
        result = dashscope_client.get_task_result(task_id)
        if result['output']['task_status'] != 'SUCCEEDED':
            continue
        time.sleep(1)
        return True, result['output']['results']
