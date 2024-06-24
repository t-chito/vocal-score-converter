from pathlib import Path

import stable_whisper # type: ignore

# settings
# Path を受け付けていないようなので、絶対パスの str で定義する
audio_file = str(Path("songs/Recreant/Recreant_cut.wav").resolve())
results_dir = Path("songs/Recreant/4stable-ts").resolve()
language = "en"

start = 18.0
end = 226.0

with open(Path("songs/Recreant/Recreant_onel.txt"), "r") as f:
    lyrics = f.read()

# Alignment https://github.com/jianfch/stable-ts?tab=readme-ov-file#alignment
model = stable_whisper.load_model("large-v2")

# アラインメントを行う
result = model.align(audio_file, lyrics, language=language)
result.to_srt_vtt(str(results_dir / "align.srt"), segment_level=False)

# 再度アラインメントを行う
new_result = model.align(audio_file, result, language=language)
new_result.to_srt_vtt(str(results_dir / "align2.srt"), segment_level=False)

# result を new_result で adjust する
result.adjust_by_result(new_result)
result.to_srt_vtt(str(results_dir / "adjusted_align.srt"), segment_level=False)

# refine する TODO: これは forced alignment なのか？ -> 多分違うのでコメントアウト
# model.refine("audio.mp3", result)
