from pathlib import Path

import whisperx # type: ignore
import whisperx.types # type: ignore

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

start=18.0
end=226.0

with open(Path("songs/Recreant/Recreant_onel.txt"), "r") as f:
  lyrics = f.read()

# 2. Align
model_a, metadata = whisperx.load_align_model(language_code=language, device=device)
audio = whisperx.load_audio(audio_file)

mock_segments:list[whisperx.types.SingleSegment] = [
    {
        "start": start,
        "end":end,
        "text": lyrics,
    },
]

result = whisperx.align(
    mock_segments,
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
write2rst(results=result, fname="annotated_alignment.srt", level="word", output_path=results_dir)

# # Clean up
# gc.collect()
# torch.cuda.empty_cache()
# del model_a



