from enum import Enum
from pathlib import Path


class SubtitleStyle(Enum):
    TIKTOK = "tiktok"
    CAPCUT = "capcut"
    MINIMAL = "minimal"
    CINEMATIC = "cinematic"


def load_style(style: SubtitleStyle) -> str:
    style_path = Path("styles") / f"{style.value}.ass"

    with open(style_path, "r", encoding="utf8") as f:
        return f.read()