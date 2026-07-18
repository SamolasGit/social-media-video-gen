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

    video_path = data.get("background_video", "assets/videos/minecraft-1.mp4")
    speed = data.get("playback_speed", 1.0)
    music_path = data.get("music")
    music_volume = float(data.get("volume", 1.0))

    if music_path is not None:
        music_file = Path(music_path)
        if not music_file.exists():
            raise FileNotFoundError(f"Music file not found: {music_path}")

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

    cmd = [
        "ffmpeg",
        "-y",
        "-ss", str(start),
        "-i", video_path,
        "-i", audio_path,
    ]

    filter_complex = None
    audio_map = ["-map", "1:a:0"]

    if music_path:
        cmd.extend(["-i", music_path])
        filter_complex = (
            f"[1:a]atempo={speed}[speech];"
            f"[2:a]atempo={speed},volume={music_volume}[music];"
            "[speech][music]amix=inputs=2:duration=shortest:dropout_transition=2[a]"
        )
        audio_map = ["-map", "[a]"]
    else:
        cmd.extend(["-af", f"atempo={speed}"])

    cmd.extend(
        [
            "-vf", vf,
            "-map", "0:v:0",
        ]
    )

    if filter_complex:
        cmd.extend(["-filter_complex", filter_complex])

    cmd.extend(
        [
            *audio_map,
            "-c:v", "libx264",
            "-preset", "medium",
            "-crf", "18",
            "-c:a", "aac",
            "-b:a", "192k",
            "-shortest",
            str(output),
        ]
    )

    subprocess.run(cmd, check=True)

    return str(output)