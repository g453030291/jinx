import json

from api.conf.config import constant

from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_alimt20181012.client import Client as alimt20181012Client
from alibabacloud_alimt20181012 import models as alimt_20181012_models
from alibabacloud_tea_util import models as util_models


class AliyunClient:
    def __init__(self):
        config = open_api_models.Config(
            access_key_id=constant.access_key_id,
            access_key_secret=constant.access_key_secret
        )
        # Endpoint 请参考 https://api.aliyun.com/product/alimt
        config.endpoint = f'mt.cn-hangzhou.aliyuncs.com'
        self.alimt_client = alimt20181012Client(config)

    # 图片翻译
    def translate_image(self, target_url, source_language, target_language, ignore_entity_recognize) -> alimt_20181012_models.TranslateImageResponse:
        translate_image_request = alimt_20181012_models.TranslateImageRequest()
        translate_image_request.image_url = target_url
        translate_image_request.source_language = source_language
        translate_image_request.target_language = target_language
        translate_image_request.ext = json.dumps({"ignoreEntityRecognize": ignore_entity_recognize})
        return self.alimt_client.translate_image_with_options(translate_image_request, util_models.RuntimeOptions())

if __name__ == '__main__':
    aliyun_client = AliyunClient()
    url = 'http://tristana-oss.oss-cn-shanghai.aliyuncs.com/2024/10/26/testpic1.jpg?OSSAccessKeyId=LTAI5tMS3r8LEYPeTe1m6sQQ&Expires=1730825233&Signature=F1TNDVvkel%2FBSbK5Q6RgZ1PDdbg%3D'
    result = aliyun_client.translate_image(url, 'en', 'zh')
    print(result)
