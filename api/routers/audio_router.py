import os
import whisperx

from urllib.parse import urlparse

from fastapi import APIRouter, Body
from loguru import logger

from api.client.oss_client import OSSClient
from api.conf import root_path
from api.conf.config import constant
from api.model.resp import Resp

router = APIRouter(prefix="/audio")

device = "cpu"
batch_size = 16
compute_type = "float32"

@router.post("/tts", response_model=Resp)
def tts(audio_url: str = Body(..., embed=True)):
    oss_client = OSSClient()
    audio_data = oss_client.get_object(urlparse(audio_url).path[1:])
    tmp_file_path = os.path.join(root_path, 'tmp', 'audio.mp3')
    with open(tmp_file_path, 'wb') as f:
        f.write(audio_data)
    asr_options = {
        "hotwords": None
    }
    model = whisperx.load_model("large-v2", device, compute_type=compute_type, asr_options=asr_options)

    audio = whisperx.load_audio(tmp_file_path)
    result = model.transcribe(audio, batch_size=batch_size)
    logger.info(result["segments"])

    model_a, metadata = whisperx.load_align_model(language_code=result["language"], device=device)
    result = whisperx.align(result["segments"], model_a, metadata, audio, device, return_char_alignments=False)

    logger.info(result["segments"])

    # diarize_model = whisperx.DiarizationPipeline(use_auth_token=constant.huggingface_token, device=device)
    #
    # diarize_segments = diarize_model(audio)
    #
    # result = whisperx.assign_word_speakers(diarize_segments, result)
    # logger.info(diarize_segments)
    os.remove(tmp_file_path)
    return Resp.success(data=result["segments"])
