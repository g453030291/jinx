import requests
from loguru import logger
from volcenginesdkarkruntime import Ark

from api.conf.config import constant

client = Ark(api_key=constant.doubao_api_key)
url = "https://ark.cn-beijing.volces.com/api/v3/chat/completions"

def completions(system_prompts, user_prompts, model="ep-20241207172944-kk7t8", image_list=None):
    if image_list:
        if not isinstance(image_list, list):
            image_list = [image_list]
        contents = [
            {
                "type": "text",
                "text": user_prompts
            }
        ]
        # Append each image to the content list
        for image_url in image_list:
            contents.append({
                "type": "image_url",
                "image_url": {
                    "url": image_url
                }
            })
        completion = requests.post(
            url=url,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {constant.doubao_api_key}"
            },
            json={
                "model": "ep-20241207172529-lnrkx",
                "messages": [
                    {
                        "role": "user",
                        "content": contents
                    }
                ]
            }
        )
        logger.info(completion.json())
        return completion.json()['choices'][0]['message']['content']
    else:
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompts},
                {"role": "user", "content": user_prompts},
            ],
        )
    return completion.choices[0].message.content

def background_generation_prompts(image_style, app_location):
    system_prompts = """你是一个负责 AI 生成商品图背景的产品经理，十分擅长根据用户需求生成一个优秀的 prompts。
这是一个用户的需求，请你生成 prompts返回。注意只返回一条合适的 prompts 即可。"""
    user_prompts = f"用户需要一个{image_style}风格的商品图背景，应用于{app_location}。"
    return completions(system_prompts=system_prompts, user_prompts=user_prompts)

if __name__ == '__main__':
    result = background_generation_prompts("自然场景", "淘宝橱窗")
    # result = completions(system_prompts="", user_prompts="看一下这两张图片里都有什么", image_list=[
    #     "http://tristana-oss.oss-cn-shanghai.aliyuncs.com/2024/12/07/WeChat4c873b73053bb6a23a0bc16997a951eb.jpg",
    #     "http://tristana-oss.oss-cn-shanghai.aliyuncs.com/2024/12/07/WeChatb1a41731ac954a691f199d7fb3737001.jpg"
    # ])
    print(result)
