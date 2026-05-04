from fastapi import FastAPI, UploadFile, File
import uvicorn

app = FastAPI()

@app.get("/")
def home():
    return {"status": "AI Brand Generator Running"}

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    return {"filename": file.filename}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=10000)
