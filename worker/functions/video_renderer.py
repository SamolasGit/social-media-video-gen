from pathlib import Path
import subprocess
import json
import random


def get_duration(path: str) -> float:
    result = subprocess.run(
        [
            "ffprobe",
            "-v", "error",
            "-show_entries", "format=duration",
            "-of", "json",
            path,
        ],
        capture_output=True,
        text=True,
        check=True,
    )

    return float(json.loads(result.stdout)["format"]["duration"])


def render_video(
    video_path: str,
    audio_path: str,
    subtitles_path: str,
    output_path: str,
    speed: float = 1.0,
):
    """
    Render a vertical short.

    speed:
        1.0 = normal
        1.25 = faster
        1.5 = much faster
        0.75 = slower
    """

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    audio_duration = get_duration(audio_path)
    video_duration = get_duration(video_path)

    final_duration = audio_duration / speed

    if video_duration > final_duration:
        start = random.uniform(
            0,
            video_duration - final_duration,
        )
    else:
        start = 0

    vf = (
        f"setpts=PTS/{speed},"
        "scale=1080:1920:force_original_aspect_ratio=increase,"
        "crop=1080:1920,"
        f"ass='{subtitles_path}'"
    )

    af = f"atempo={speed}"

    cmd = [
        "ffmpeg",
        "-y",

        "-ss",
        str(start),

        "-i",
        video_path,

        "-i",
        audio_path,

        "-vf",
        vf,

        "-af",
        af,

        "-map",
        "0:v:0",

        "-map",
        "1:a:0",

        "-c:v",
        "libx264",

        "-preset",
        "medium",

        "-crf",
        "18",

        "-c:a",
        "aac",

        "-b:a",
        "192k",

        "-shortest",

        str(output),
    ]

    subprocess.run(cmd, check=True)

    return str(output)