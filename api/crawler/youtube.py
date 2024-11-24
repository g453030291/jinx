import os
import re
import uuid

from fastapi import APIRouter, Body

import yt_dlp

from api.client.oss_client import OSSClient
from api.conf import root_path
from api.model.resp import Resp
from api.util.file_util import clear_files_with_extension, get_files_with_extension

router = APIRouter()


@router.post("/youtube/download", response_model=Resp)
def youtube_download(urls: list[str] = Body(..., embed=True)):
    results_list = []
    oss_client = OSSClient()
    tmp_path = os.path.join(root_path, 'tmp')

    ydl_opts = {
        'match_filter': longer_than_a_minute,
        'outtmpl': os.path.join(tmp_path, '%(title)s.%(ext)s'),
        'verbose': True,
        'sanitize_filename': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        for url in urls:
            ydl.extract_info(url, download=True)

    for video_path in get_files_with_extension(tmp_path, '.webm'):
        with open(video_path, 'rb') as f:
            oss_url = oss_client.put_object(os.path.basename(video_path), f.read())
            results_list.append(oss_url)

    # clean up
    clear_files_with_extension(tmp_path, 'webm')
    return Resp.success(data=results_list)

def longer_than_a_minute(info, *, incomplete):
    """Download only videos longer than a minute (or with unknown duration)"""
    duration = info.get('duration')
    if duration and duration < 60:
        return 'The video is too short'


if __name__ == '__main__':
    youtube_download(['https://www.youtube.com/watch?v=fy-bd5AC-Ms'])
