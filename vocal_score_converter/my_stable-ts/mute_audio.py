from pathlib import Path

# Warning が出るけど、無視しても問題ない
# https://github.com/jiaaro/pydub/issues/790
# https://github.com/jiaaro/pydub/pull/504
from pydub import AudioSegment

MuteSegments = list[tuple[int, int | None]]


def mute_audio(
    input_wav_path: Path, output_wav_path: Path, mute_segments: MuteSegments
):
    # 音声ファイルを読み込む
    audio = AudioSegment.from_wav(input_wav_path)

    for start_sec, end_sec in mute_segments:
        mute_start_msec = to_milliseconds(start_sec)
        # None の場合は音声ファイルの最後を指定する
        mute_end_msec = len(audio) - 1 if end_sec is None else to_milliseconds(end_sec)

        # 指定範囲を無音にする
        silence = AudioSegment.silent(duration=mute_end_msec - mute_start_msec)
        audio = audio[:mute_start_msec] + silence + audio[mute_end_msec:]

    # 無音にした音声ファイルを保存する
    audio.export(output_wav_path, format="wav")


def to_milliseconds(seconds: float) -> int:
    return int(seconds * 1000)


if __name__ == "__main__":
    input_wav_path = Path("songs/Recreant/Recreant.wav")
    output_wav_path = Path("songs/Recreant/Recreant_cut.wav")
    mute_segments: MuteSegments = [(0, 18), (226, None)]

    mute_audio(input_wav_path, output_wav_path, mute_segments)
