from openai.types.audio import TranscriptionWord
from styles.subtitles_styles import SubtitleStyle, load_style
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()
def transcribe_audio(audio_file: str):
    with open(audio_file, "rb") as f:
        return client.audio.transcriptions.create(
            model="whisper-1",
            file=f,
            response_format="verbose_json",
            timestamp_granularities=["word"],
        )

def ass_timestamp(seconds: float) -> str:
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    cs = int(round((seconds - int(seconds)) * 100))

    return f"{h}:{m:02}:{s:02}.{cs:02}"


def generate_ass(
    words: list[TranscriptionWord],
    output_file: str,
    style: SubtitleStyle = SubtitleStyle.TIKTOK,
    speed: float = 1.0,
):
    style_text = load_style(style)

    with open(output_file, "w", encoding="utf8") as f:

        f.write("[Script Info]\n")
        f.write("ScriptType: v4.00+\n")
        f.write("PlayResX: 1080\n")
        f.write("PlayResY: 1920\n\n")

        f.write(style_text)

        f.write("\n\n[Events]\n")
        f.write(
            "Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text\n"
        )

        sentence = []

        for word in words:

            sentence.append(word.word)

            visible = sentence[-4:]

            parts = visible.copy()

            parts[-1] = (
                r"{\c&H00FFFF&\fscx70\fscy70\t(0,120,\fscx100\fscy100)}"
                + parts[-1]
                + r"{\c&HFFFFFF&}"
            )

            text = " ".join(parts)

            start = word.start / speed
            end = word.end / speed

            f.write(
                f"Dialogue: 0,"
                f"{ass_timestamp(start)},"
                f"{ass_timestamp(end)},"
                f"Default,,0,0,0,,{text}\n"
            )