from pathlib import Path
from typing import Literal

import whisperx.types  # type: ignore

# https://github.com/m-bain/whisperX/issues/398
# score は使い道なさそうなのでこのまま無視

# TODO: 時間表記のフォーマットを srt に合わせる
# いまだと 19.04 --> 26.241 のようになっているが、
# 00:00:19,040 --> 00:00:26,241 の表記が正しい

def write2rst(
    results: whisperx.types.AlignedTranscriptionResult,
    fname: str,
    level: Literal["word", "char"],
    output_path=Path("songs/Recreant/4whisper-x"),
):
    text_segments = results["segments"]

    with open(output_path / fname, mode="w", newline="") as file:
        index = 1
        # text 単位の segment の中に words/chars 単位の segment がある
        for text_segment in text_segments:
            target_segments = text_segment[level + "s"]
            for target_segment in target_segments:
                file.write(f"{index}\n")
                file.write(f"{target_segment['start']} --> {target_segment['end']}\n")
                file.write(f"{target_segment[level]}\n\n")
                index += 1
