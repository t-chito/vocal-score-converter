# import csv
import gc
from pathlib import Path

import torch
import whisperx # type: ignore

from save_alignment_results import write2rst # type: ignore

# https://github.com/m-bain/whisperX/blob/main/README.md#python-usage--

# 0. settings

## resources
device = "cuda"
batch_size = 16
compute_type = "float16"

## songs
audio_file = Path("songs/Recreant/Recreant.wav")
results_dir = Path("songs/Recreant/4whisper-x")
language = "en"
return_char_alignments = False

# 1. Transcribe
model = whisperx.load_model("large-v2", device, compute_type=compute_type)
audio = whisperx.load_audio(audio_file)

result = model.transcribe(audio, batch_size=batch_size, language=language)
# print("--- Transcription ---")
# print(result["segments"])
# print("--- Transcription ---")

## Save results
## https://github.com/m-bain/whisperX/issues/342
with open(results_dir/"transcription.srt", "w", encoding="utf-8") as srt:
    writesrt=whisperx.utils.WriteSRT(results_dir)
    writesrt.write_result(result=result, file=srt,options={"max_line_width":None,"max_line_count":None,"highlight_words":False})

## Clean up
gc.collect()
torch.cuda.empty_cache()
del model

# 2. Align
model_a, metadata = whisperx.load_align_model(language_code=language, device=device)
result = whisperx.align(
    result["segments"],
    model_a,
    metadata,
    audio,
    device,
    return_char_alignments=return_char_alignments,
)

# print("--- Alignment Result ---")
# print(result["word_segments"])
# print("--- Alignment Result ---")

## Save results
write2rst(results=result, fname="rough_alignment.srt", level="word", output_path=results_dir)

# Clean up
gc.collect()
torch.cuda.empty_cache()
del model_a



