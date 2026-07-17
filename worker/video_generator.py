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
from styles.subtitles_styles import SubtitleStyle

TMP_DIR = Path("tmp")
OUTPUT_DIR = Path("output")

TMP_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)


def generate_video(data, job_id: str):

    audio_file = TMP_DIR / f"{job_id}_audio.mp3"
    subtitles_file = TMP_DIR / f"{job_id}_subtitles.ass"
    output_file = OUTPUT_DIR / f"{job_id}.mp4"

    prompt = load_prompt(
        data["prompt"],
        theme=data["theme"],
        guide=data["guide"]
    )

    instructions = load_instruction(
        data["instruction"]
    )

    script = generate_script(
        model="gpt-4.1-mini",
        instructions=instructions,
        input_text=prompt
    )

    generate_tts(
        text=script,
        output_file=str(audio_file),
        voice=data["voice"]
    )

    transcript = transcribe_audio(
        str(audio_file)
    )

    generate_ass(
        words=transcript.words,
        output_file=str(subtitles_file),
        style=SubtitleStyle(data["subtitle_style"])
    )

    render_video(
        video_path=data["background_video"],
        audio_path=str(audio_file),
        subtitles_path=str(subtitles_file),
        output_path=str(output_file)
    )

    return output_file