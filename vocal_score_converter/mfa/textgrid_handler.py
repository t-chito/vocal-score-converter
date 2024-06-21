"""textgrid を扱うモジュール"""

import csv
from pathlib import Path
from typing import Literal

import pysrt  # type: ignore
from textgrid import TextGrid  # type: ignore


def textgrid_to_csv(
    textgrid_path, csv_path, use_only_tier: Literal["words", "phones"] | None = None
):
    tg = TextGrid.fromFile(textgrid_path)

    with open(csv_path, mode="w", newline="") as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["Tier", "Start", "End", "Text"])

        for tier in tg:
            # words または phones のみを使う場合
            if use_only_tier and tier.name != use_only_tier:
                continue

            for interval in tier.intervals:
                csv_writer.writerow(
                    [tier.name, interval.minTime, interval.maxTime, interval.mark]
                )


def textgrid_to_srt(textgrid_path, srt_path):
    tg = TextGrid.fromFile(textgrid_path)
    srt_subs = pysrt.SubRipFile()

    for tier in tg:
        for interval in tier:
            if interval.mark.strip():  # 空白でないマークのみ処理
                start_time = interval.minTime
                end_time = interval.maxTime
                text = interval.mark

                start_hours, start_remainder = divmod(start_time, 3600)
                start_minutes, start_seconds = divmod(start_remainder, 60)
                start_milliseconds = (start_seconds - int(start_seconds)) * 1000

                end_hours, end_remainder = divmod(end_time, 3600)
                end_minutes, end_seconds = divmod(end_remainder, 60)
                end_milliseconds = (end_seconds - int(end_seconds)) * 1000

                start_time_str = f"{int(start_hours):02}:{int(start_minutes):02}:{int(start_seconds):02},{int(start_milliseconds):03}"
                end_time_str = f"{int(end_hours):02}:{int(end_minutes):02}:{int(end_seconds):02},{int(end_milliseconds):03}"

                subtitle = pysrt.SubRipItem(
                    index=len(srt_subs) + 1,
                    start=start_time_str,
                    end=end_time_str,
                    text=text,
                )
                srt_subs.append(subtitle)

    srt_subs.save(srt_path, encoding="utf-8")


# 使用例


if __name__ == "__main__":
    input_textgrid_path = Path("songs/Recreant/4mfa/results/Recreant.TextGrid")
    output_dir = Path("songs/Recreant/4mfa/results")

    textgrid_to_csv(
        input_textgrid_path, output_dir / "Recreant.csv", use_only_tier="words"
    )
    textgrid_to_srt(
        input_textgrid_path,
        output_dir / "Recreant.srt",
    )
