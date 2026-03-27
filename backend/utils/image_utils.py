import io
from PIL import Image
from google import genai
from config import settings

client = genai.Client(api_key=settings.gemini_api_key)

client = genai.Client()

prompt = ("Create a picture of a nano banana dish in a fancy restaurant with a Gemini theme")
response = client.models.generate_content(
    model="gemini-2.5-flash-image-preview",
    contents=[prompt]
)
for part in response.parts:
    if part.text is not None:
        print(part.text)
    elif part.inline_data is not None:
        image = part.as_image()
        image.save("generated_image.png")

buffer = io.BytesIO()
image.save(buffer, format="PNG")
buffer.seek(0)
Image.open(buffer).show()
