from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import base64
from pydantic import BaseModel
class AudioRequest(BaseModel):
    audio_base64: str
    language: str


app = FastAPI()

# Allow hackathon website + Postman
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/detect")
async def detect(payload: AudioRequest):
    

    language = payload.language
    audio_format = payload.audio_format
    audio_base64 = payload.audio_base64

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

