from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

def generate_script(
    model,
    instructions,
    input_text,
    language="en",
):
    response = client.responses.create(
        model=model,
        instructions=f"""
{instructions}

Write the entire response in {language}.
Do not mix languages.
""",
        input=input_text,
    )

    return response.output_text