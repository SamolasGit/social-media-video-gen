from pathlib import Path

STYLES_DIR = Path(__file__).parent

def load_style(style_name: str) -> str:
    style_path = STYLES_DIR / f"{style_name}.ass"

    if not style_path.exists():
        available = [p.stem for p in STYLES_DIR.glob("*.ass")]
        raise ValueError(
            f"Unknown subtitle style: {style_name}. "
            f"Available styles: {', '.join(sorted(available))}"
        )

    return style_path.read_text(encoding="utf-8")