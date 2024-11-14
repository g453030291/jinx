# import whisperx
# from PIL import Image
# from controlnet_aux.processor import Processor
#
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
#     diarize_model = whisperx.DiarizationPipeline(use_auth_token='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', device=device)
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
