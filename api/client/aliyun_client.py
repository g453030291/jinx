import asyncio
import json

from api.conf.config import constant
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_alimt20181012.client import Client as alimt20181012Client
from alibabacloud_imageseg20191230.client import Client as imageseg20191230Client
from alibabacloud_alimt20181012 import models as alimt_20181012_models
from alibabacloud_imageseg20191230.models import SegmentCommodityRequest, SegmentCommodityResponse
from alibabacloud_tea_util import models as util_models


class AliyunClient:
    def __init__(self):
        self.alimt_client = self.create_client('mt.cn-hangzhou.aliyuncs.com', alimt20181012Client)
        self.segment_client = self.create_client('imageseg.cn-shanghai.aliyuncs.com', imageseg20191230Client)

    def create_client(self, endpoint, client_class):
        config = open_api_models.Config(
            access_key_id=constant.access_key_id,
            access_key_secret=constant.access_key_secret
        )
        config.endpoint = endpoint
        return client_class(config)

    # 图片翻译
    async def translate_image(self, target_url, source_language, target_language, ignore_entity_recognize) -> alimt_20181012_models.TranslateImageResponse:
        translate_image_request = alimt_20181012_models.TranslateImageRequest()
        translate_image_request.image_url = target_url
        translate_image_request.source_language = source_language
        translate_image_request.target_language = target_language
        translate_image_request.ext = json.dumps({"ignoreEntityRecognize": ignore_entity_recognize})
        return await self.alimt_client.translate_image_with_options_async(translate_image_request, util_models.RuntimeOptions())

    # 商品分割
    async def segment_commodity(self, url) -> SegmentCommodityResponse:
        segment_commodity_request = SegmentCommodityRequest()
        segment_commodity_request.image_url = url
        return await self.segment_client.segment_commodity_with_options_async(segment_commodity_request, util_models.RuntimeOptions())

async def test():
    aliyun_client = AliyunClient()
    url = 'https://tristana-oss.oss-cn-shanghai.aliyuncs.com/2024/12/14/test_pic1.jpg'
    # result = await aliyun_client.translate_image(url, 'en', 'zh', False)
    # print(result)
    result = await aliyun_client.segment_commodity(url)
    print(result)

if __name__ == '__main__':
    asyncio.run(test())
