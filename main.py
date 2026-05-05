from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from openai import OpenAI
import os
import base64

app = FastAPI()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Serve frontend UI
@app.get("/")
def serve_ui():
    return FileResponse("index.html")

# Optional: health check route
@app.get("/status")
def status():
    return {"status": "AI Brand Generator LIVE"}

@app.post("/generate")
async def generate(file: UploadFile = File(...)):
    image_bytes = await file.read()
    base64_image = base64.b64encode(image_bytes).decode("utf-8")

    # AI TEXT
    text = client.chat.completions.create(
        model="gpt-5",
        messages=[
            {"role": "user", "content": "Create a professional CEO bio, tagline, and brand identity."}
        ]
    )

    # AI IMAGE
    image = client.images.generate(
        model="gpt-image-1",
        prompt="professional CEO portrait, suit, luxury office, cinematic lighting",
        size="1024x1024"
    )

    return {
        "bio": text.choices[0].message.content,
        "image": image.data[0].url
    }
