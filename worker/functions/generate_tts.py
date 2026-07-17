from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()
def generate_tts(
    text: str,
    output_file: str,
    model: str = "gpt-4o-mini-tts",
    voice: str = "alloy",
) -> str:
    response = client.audio.speech.create(
        model=model,
        voice=voice,
        input=text,
    )

    response.stream_to_file(output_file)

    return output_file