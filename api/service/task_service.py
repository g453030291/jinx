from sqlalchemy import false


# 图片翻译任务
def translate_image(aliyun_client, url, source_language, target_language):
    result = aliyun_client.translate_image(url, source_language, target_language)
    if result.status_code != 200:
        return False, result.data.message
    return True, result.body.data.final_image_url
