"""textgrid を扱うモジュール"""

import csv
from pathlib import Path

from textgrid import TextGrid  # type: ignore


def textgrid_to_csv(textgrid_path, csv_path):
    tg = TextGrid.fromFile(textgrid_path)

    with open(csv_path, mode="w", newline="") as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["Tier", "Start", "End", "Text"])

        for tier in tg:
            for interval in tier.intervals:
                csv_writer.writerow(
                    [tier.name, interval.minTime, interval.maxTime, interval.mark]
                )


if __name__ == "__main__":
    textgrid_path = Path("songs/Recreant/4mfa/Recreant.TextGrid")
    csv_path = Path("songs/Recreant/4mfa/Recreant.csv")
    textgrid_to_csv(textgrid_path, csv_path)
