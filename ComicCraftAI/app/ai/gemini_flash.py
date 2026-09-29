import os
from dotenv import load_dotenv

load_dotenv()

from google import genai
import base64
from google import genai
import base64
import os

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def generate_image(prompt: str):
    interaction = client.interactions.create(
        model="gemini-3.1-flash-image",
        input=prompt,
    )

    image_data = base64.b64decode(interaction.output_image.data)

    with open("generated_image.png", "wb") as f:
        f.write(image_data)

    return "generated_image.png"