from pathlib import Path

from functions.generate_script import generate_script
from functions.generate_tts import generate_tts
from functions.generate_subtitles import (
    transcribe_audio,
    generate_ass,
)
from functions.video_renderer import render_video
from functions.prompt_loader import (
    load_prompt,
    load_instruction,
)
TMP_DIR = Path("tmp")
OUTPUT_DIR = Path("output")

TMP_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)


def generate_video(data, job_id: str):

    audio_file = TMP_DIR / f"{job_id}_audio.mp3"
    subtitles_file = TMP_DIR / f"{job_id}_subtitles.ass"
    output_file = OUTPUT_DIR / f"{job_id}.mp4"

    prompt = load_prompt(
        data.get("prompt", "reddit_story"),
        theme=data.get("theme", ""),
        guide=data.get("guide", "")
    )

    instructions = load_instruction(
        data.get("instruction", "tiktok")
    )

    script = generate_script(
        model="gpt-4.1-mini",
        instructions=instructions,
        input_text=prompt,
        language=data.get("language", "en"),
    )

    generate_tts(
        text=script,
        output_file=str(audio_file),
        voice=data.get("voice", "alloy")
    )

    transcript = transcribe_audio(
        str(audio_file),
        language=data.get("language", "en"),
    )

    if not transcript.words:
        raise RuntimeError("Whisper did not return word timestamps.")

    generate_ass(
        words=transcript.words,
        output_file=str(subtitles_file),
        style=data.get("subtitle_style", "tiktok"),
    )
    render_video(
        data=data,
        audio_path=str(audio_file),
        subtitles_path=str(subtitles_file),
        output_path=str(output_file),
    )

    return output_file