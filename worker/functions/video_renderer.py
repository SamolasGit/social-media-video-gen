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
    data: dict,
    audio_path: str,
    subtitles_path: str,
    output_path: str,
):
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    video_path = data["background_video"]
    speed = data["playback_speed"]

    audio_duration = get_duration(audio_path)
    video_duration = get_duration(video_path)

    final_duration = audio_duration / speed

    start = (
        random.uniform(0, video_duration - final_duration)
        if video_duration > final_duration
        else 0
    )

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
        "-ss", str(start),
        "-i", video_path,
        "-i", audio_path,
        "-vf", vf,
        "-af", af,
        "-map", "0:v:0",
        "-map", "1:a:0",
        "-c:v", "libx264",
        "-preset", "medium",
        "-crf", "18",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        str(output),
    ]

    subprocess.run(cmd, check=True)

    return str(output)