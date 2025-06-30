
from groq import Groq
import base64
import os
from dotenv import load_dotenv

def extract_text_from_image(image_path):
    load_dotenv()
    api_key = os.getenv("GROQ_PLAG_API")
    if not api_key:
        raise ValueError("GROQ_PLAG_API not set in .env file")
    client = Groq(api_key=api_key)
    with open(image_path, "rb") as image_file:
        base64_image = base64.b64encode(image_file.read()).decode('utf-8')
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Do not answer any questions other than to Extract the text as it is looking in the image. Remember if the text is handwritten, you should not try to correct it or change it. Just extract the text as it is."},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}",
                        },
                    },
                ],
            }
        ],
        model="meta-llama/llama-4-scout-17b-16e-instruct",
    )
    return chat_completion.choices[0].message.content

if __name__ == "__main__":
    # For standalone testing only
    image_path = "full-page.png"
    print(extract_text_from_image(image_path))