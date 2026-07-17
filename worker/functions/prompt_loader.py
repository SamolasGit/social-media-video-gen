from pathlib import Path

PROMPTS_DIR = Path("prompts")
INSTRUCTIONS_DIR = Path("instructions")


def load_prompt(name: str, **kwargs) -> str:
    path = PROMPTS_DIR / f"{name}.txt"

    if not path.exists():
        raise FileNotFoundError(f"Prompt '{name}' not found.")

    text = path.read_text(encoding="utf-8")

    return text.format(**kwargs)


def load_instruction(name: str) -> str:
    path = INSTRUCTIONS_DIR / f"{name}.txt"

    if not path.exists():
        raise FileNotFoundError(f"Instruction '{name}' not found.")

    return path.read_text(encoding="utf-8")