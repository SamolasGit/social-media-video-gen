from pathlib import Path

STYLES_DIR = Path(__file__).parent / "styles"

def load_style(style_name: str) -> str:
    style_path = STYLES_DIR / f"{style_name}.ass"

    if not style_path.exists():
        raise ValueError(f"Unknown subtitle style: {style_name}")

    return style_path.read_text(encoding="utf-8")