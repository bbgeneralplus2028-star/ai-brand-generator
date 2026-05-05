from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import FileResponse
from openai import OpenAI
import os

app = FastAPI()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.get("/")
def serve_ui():
    return FileResponse("index.html")

@app.get("/status")
def status():
    return {"status": "LIVE"}

@app.post("/generate")
async def generate(
    file: UploadFile = File(...),
    style: str = Form(...),
    hat: str = Form(...)
):
    await file.read()

    # STYLE PROMPT LOGIC
    prompt = "professional CEO portrait, high quality"

    if style == "luxury":
        prompt += ", luxury office, gold tones, cinematic lighting"
    elif style == "corporate":
        prompt += ", corporate office, clean background"
    elif style == "street":
        prompt += ", modern entrepreneur, urban style"

    if hat == "yes":
        prompt += ", wearing a stylish hat"

    # AI TEXT
    text = client.chat.completions.create(
        model="gpt-5",
        messages=[
            {"role": "user", "content": f"Create a CEO bio and brand profile for a {style} business leader."}
        ]
    )

    # MULTIPLE IMAGES
    images = []
    for i in range(3):
        img = client.images.generate(
            model="gpt-image-1",
            prompt=prompt,
            size="1024x1024"
        )
        images.append(img.data[0].url)

    # LOGO GENERATOR (simple)
    logo = client.images.generate(
        model="gpt-image-1",
        prompt="modern corporate logo, BHR Services LLC, minimalist, gold and black",
        size="512x512"
    )

    return {
        "bio": text.choices[0].message.content,
        "images": images,
        "logo": logo.data[0].url
    }
