import stable_whisper # type: ignore

from pathlib import Path

import shutil


audio_file = str(Path("songs/Recreant/Recreant.wav").resolve())

srt1_path = shutil.copy(Path("songs/Recreant/4stable-ts/adjusted_align.srt"), 'stable-ts.srt')
srt2_path = shutil.copy(Path("songs/Recreant/4mfa/results/Recreant.srt"), 'mfa.srt')
# srt3_path = shutil.copy(Path("songs/Recreant/4whisper-x/annotated_alignment.srt"), 'whisper-x.srt')
# srt3_path = "whisper-x-converted.srt"
srt3_path = "whisper-x-converted-time.srt"

output_videopath = str(Path("songs/Recreant/comparison").resolve() / "comparison.mp4")

# 動かないので cmd に吐き出してから手動で実行する
# TODO: 自分で subprocess を書いても良い
cmd = stable_whisper.encode_video_comparison(
    audio_file, 
    [srt1_path, srt2_path, srt3_path     ], 
    output_videopath=output_videopath, 
    # labels=['Example 1', 'Example 2']
    only_cmd=True
)

print(cmd)