from api.conf.config import constant

import requests
import json

# aliyun 百炼大模型

# 生成背景
# base_image_url必传,
# ref_image_url, ref_prompt必传一个
def generate_background(base_image_url, ref_image_url, ref_prompt, foreground_edges=None, background_edges=None,
                    foreground_edge_prompts=None, background_edge_prompts=None):
    url = 'https://dashscope.aliyuncs.com/api/v1/services/aigc/background-generation/generation/'
    headers = {
        'X-DashScope-Async': 'enable',
        'Authorization': f'Bearer {constant.ali_bai_lian_api_key}',
        'Content-Type': 'application/json'
    }
    data = {
        "model": 'wanx-background-generation-v2',
        "input": {
            "base_image_url": base_image_url,
            "reference_edge": {}
        }
    }
    if ref_image_url is not None:
        data["input"]["ref_image_url"] = ref_image_url
    if ref_prompt is not None:
        data["input"]["ref_prompt"] = ref_prompt
    if foreground_edges is not None:
        data["input"]["reference_edge"]["foreground_edge"] = foreground_edges
    if background_edges is not None:
        data["input"]["reference_edge"]["background_edge"] = background_edges
    if foreground_edge_prompts is not None:
        data["input"]["reference_edge"]["foreground_edge_prompt"] = foreground_edge_prompts
    if background_edge_prompts is not None:
        data["input"]["reference_edge"]["background_edge_prompt"] = background_edge_prompts

    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.json()

# 查询任务结果
# GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}
def get_task_result(task_id):
    url = f'https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}'
    headers = {
        'Authorization': f'Bearer {constant.ali_bai_lian_api_key}'
    }
    response = requests.get(url, headers=headers)
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

if __name__ == '__main__':
    # response = generate_background(base_image_url=base_image_url, ref_image_url=ref_image_url, ref_prompt=None)
    # print(response)
    # task_id = response['output']['task_id']
    result = get_task_result('99c7a783-19f7-4816-8b4a-4434df34286c')
    print(result)
