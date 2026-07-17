from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

def generate_script(model, instructions, input_text):
    response = client.responses.create(
        model=model,
        instructions=instructions,
        input=input_text
    )
    return response.output_text
