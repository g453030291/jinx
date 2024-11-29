# import whisperx
# from PIL import Image
# from controlnet_aux.processor import Processor
# #
# def make_elements(name):
#     hed_processor = Processor('softedge_hed')
#     img = Image.open(name)
#     if img.mode == 'RGBA':
#         r, g, b, a = img.split()
#         img = img.convert('RGB')
#         hed_img = hed_processor(img, to_pil=True).resize(img.size).convert('RGB')
#         hed_img.putalpha(a)
#     else:
#         img = img.convert('RGB')
#         hed_img = hed_processor(img, to_pil=True).resize(img.size).convert('RGB')
#     hed_img.save('/Users/gemushen/test-file/make_elements/result1.png')
#
# device = "cpu"
# audio_file = "/Users/gemushen/test-file/Blank Space-2.mp3"
# batch_size = 16 # reduce if low on GPU mem
# compute_type = "float32" # change to "int8" if low on GPU mem (may reduce accuracy)
#
# def whisperx_test():
#     # 1. Transcribe with original whisper (batched)
#     model = whisperx.load_model("large-v2", device, compute_type=compute_type)
#
#     # save model to local path (optional)
#     # model_dir = "/path/"
#     # model = whisperx.load_model("large-v2", device, compute_type=compute_type, download_root=model_dir)
#
#     audio = whisperx.load_audio(audio_file)
#     result = model.transcribe(audio, batch_size=batch_size)
#     print(result["segments"])  # before alignment
#
#     # delete model if low on GPU resources
#     # import gc; gc.collect(); torch.cuda.empty_cache(); del model
#
#     # 2. Align whisper output
#     model_a, metadata = whisperx.load_align_model(language_code="en", device=device)
#     result = whisperx.align(result["segments"], model_a, metadata, audio, device, return_char_alignments=False)
#
#     print(result["segments"])  # after alignment
#
#     # delete model if low on GPU resources
#     # import gc; gc.collect(); torch.cuda.empty_cache(); del model_a
#
#     # 3. Assign speaker labels
#     diarize_model = whisperx.DiarizationPipeline(use_auth_token='hf_IbaegCSGDYFEpCkXOKDpbSkIrsgUEQh', device=device)
#
#     # add min/max number of speakers if known
#     diarize_segments = diarize_model(audio)
#     # diarize_model(audio, min_speakers=min_speakers, max_speakers=max_speakers)
#
#     result = whisperx.assign_word_speakers(diarize_segments, result)
#     print(diarize_segments)
#     print(result["segments"])  # segments are now assigned speaker IDs
#
# if __name__ == '__main__':
#     # make_elements('/Users/gemushen/test-file/make_elements/Gb3zWbHaMAArlzJ.jpeg')
#     whisperx_test()
import json

import yagmail
import yt_dlp

from api.conf import root_path


def youtube():
    URLS = ['https://www.bilibili.com/video/BV1UBUHYTEqS/?spm_id_from=333.1007.tianma.2-1-4.click&vd_source=3db5c9c9957e313b7098ea2b30d5b0c3']

    def longer_than_a_minute(info, *, incomplete):
        """Download only videos longer than a minute (or with unknown duration)"""
        duration = info.get('duration')
        if duration and duration < 60:
            return 'The video is too short'

    ydl_opts = {
        'match_filter': longer_than_a_minute,
        'format': 'bestvideo+bestaudio/best',
        'cookiefile': 'www.bilibili.com_cookies.txt',
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        error_code = ydl.download(URLS)

def send_email():
    yag = yagmail.SMTP('80a951001@smtp-brevo.com', 'WMxmy3dNTHS6XhYq', host='smtp-relay.brevo.com', port=587)
    to = '453030291@qq.com'
    subject = '验证码'
    body = '这是一个登录验证码:ABCD'
    # html = '<a href="https://pypi.python.org/pypi/sky/">Click me!</a>'
    # img = '/local/file/bunny.png'
    yag.send(to=to, subject=subject, contents=[body])


YOUR_API_KEY = ""

from __future__ import print_function
import time
import brevo_python
from brevo_python.rest import ApiException
from pprint import pprint

def send_brevo_email():
    # Configure API key authorization: api-key
    configuration = brevo_python.Configuration()
    configuration.api_key['api-key'] = YOUR_API_KEY
    # Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
    # configuration.api_key_prefix['api-key'] = 'Bearer'
    # Configure API key authorization: partner-key
    configuration = brevo_python.Configuration()
    configuration.api_key['partner-key'] = YOUR_API_KEY
    # Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
    # configuration.api_key_prefix['partner-key'] = 'Bearer'

    # create an instance of the API class
    api_instance = brevo_python.EmailCampaignsApi(brevo_python.ApiClient(configuration))
    campaign_id = 789 # int | Id of the campaign
    email_to = brevo_python.SendTestEmail() # SendTestEmail |

    try:
        # Send an email campaign to your test list
        api_instance.send_test_email(campaign_id, email_to)
    except ApiException as e:
        print("Exception when calling EmailCampaignsApi->send_test_email: %s\n" % e)

if __name__ == '__main__':
    # youtube()
    send_email()
