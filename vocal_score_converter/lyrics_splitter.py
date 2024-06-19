"""歌詞を syllable 単位で分割するモジュール"""

import re
from pathlib import Path
from typing import Any, Literal

import pyphen  # type: ignore

# 歌詞のセクション
Section = Literal["Intro", "Verse", "Pre-Chorus", "Chorus", "Bridge", "Outro"]

# 歌詞
Lyrics = list[tuple[Section, str]]

# シラブル
Syllables = list[tuple[Section, list[str]]]

BASE_DIR = Path(__file__).resolve().parent / ".." / "songs"


def load_lyrics(song_name: str) -> str:
    file_path = BASE_DIR / song_name / "lyrics.txt"
    with open(file_path, "r") as f:
        lyrics_str = f.read()
    return lyrics_str


def parse_lyrics(lyrics_str: str) -> Lyrics:
    # 歌詞をセクションごとに分割
    sections = re.split(r"\[(.*?)\]", lyrics_str)
    # セクションごとに歌詞を分割
    lyrics = []
    for i in range(1, len(sections), 2):
        section: Any = sections[i]
        lyrics.append((section, sections[i + 1]))
    return lyrics


dic = pyphen.Pyphen(lang="en")


def split_lyrics_into_syllables(lyrics: Lyrics) -> Syllables:
    # 歌詞をシラブル単位に分割
    syllables = []

    for section, text in lyrics:
        _syllables: list[str] = []

        words = text.split()
        for word in words:
            _syllables += dic.inserted(word).split("-")

        syllables.append((section, _syllables))

    return syllables


if __name__ == "__main__":
    lyrics_str = load_lyrics("Recreant")
    lyrics = parse_lyrics(lyrics_str)
    print(lyrics)
    syllables = split_lyrics_into_syllables(lyrics)
    print(syllables)
