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

if __name__ == '__main__':
    result = completions(system_prompts="", user_prompts="看一下这两张图片里都有什么", image_list=[
        "http://tristana-oss.oss-cn-shanghai.aliyuncs.com/2024/12/07/WeChat4c873b73053bb6a23a0bc16997a951eb.jpg",
        "http://tristana-oss.oss-cn-shanghai.aliyuncs.com/2024/12/07/WeChatb1a41731ac954a691f199d7fb3737001.jpg"
    ])
    print(result)
