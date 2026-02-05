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
    "classification": "HUMAN_GENERATED",
    "confidence": 0.51,
    "explanation": {
        "spectral_artifacts": "Not analyzed yet",
        "prosody_analysis": "Not analyzed yet",
        "language_consistency": "Not analyzed yet",
        "model_reasoning": "Baseline response before AI model integration"
    },
    "metadata": {
        "language": req.language,
        "duration_seconds": round(len(audio) / sr, 2),
        "sample_rate": sr
    }
}

