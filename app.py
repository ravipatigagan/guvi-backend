from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import base64

app = FastAPI()

# Allow hackathon website + Postman
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/detect")
async def detect(request: Request):
    data = await request.json()

    language = data.get("language")
    audio_format = data.get("audio_format")
    audio_base64 = data.get("audio_base64")

    if not audio_base64:
        return {"error": "audio_base64 missing"}

    # Just validate base64 (no processing yet)
    try:
        base64.b64decode(audio_base64)
    except:
        return {"error": "Invalid base64 audio"}

    return {
    "classification": "Human-generated",
    "confidence": 0.50,
    "language": payload.language,
    "explanation": "Baseline response — AI analysis not yet applied",
    "audio_format": "mp3",
    "processing_time_ms": 0
}


@app.get("/")
def root():
    return {
        "status": "running",
        "service": "AI Voice Detector API",
        "health": "OK"
    }

