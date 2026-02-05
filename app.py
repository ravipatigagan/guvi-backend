from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import base64
from pydantic import BaseModel
from typing import Optional
import numpy as np
import librosa
import io
import time

class AudioRequest(BaseModel):
    audio_base64: str
    language: str
    audio_format: Optional[str] = None

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/detect")
async def detect(payload: AudioRequest):

    start_time = time.time()

    # Decode base64
    try:
        audio_bytes = base64.b64decode(payload.audio_base64)
        audio_buffer = io.BytesIO(audio_bytes)

        # Load audio safely
        y, sr = librosa.load(audio_buffer, sr=None)

    except Exception as e:
        return {"error": "Audio decoding failed", "details": str(e)}

    # ===============================
    # FEATURE EXTRACTION (FORENSICS)
    # ===============================

    # Pitch (fundamental frequency)
    pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
    pitch_variance = np.var(pitches[pitches > 0]) if np.any(pitches > 0) else 0

    # Spectral entropy proxy
    spectral_centroid = np.mean(librosa.feature.spectral_centroid(y=y, sr=sr))

    # Zero-crossing rate (AI voices are unnaturally smooth)
    zcr = np.mean(librosa.feature.zero_crossing_rate(y))

    # ===============================
    # SCORING LOGIC (Explainable AI)
    # ===============================

    ai_score = 0

    if pitch_variance < 50:
        ai_score += 1

    if spectral_centroid < 1500:
        ai_score += 1

    if zcr < 0.05:
        ai_score += 1

    classification = "AI-generated" if ai_score >= 2 else "Human-generated"
    confidence = min(0.95, 0.55 + (ai_score * 0.15))

    explanation = (
        "Low pitch variance and spectral smoothness detected"
        if classification == "AI-generated"
        else "Natural pitch fluctuations and entropy indicate human speech"
    )

    processing_time = int((time.time() - start_time) * 1000)

    return {
        "classification": classification,
        "confidence": round(confidence, 2),
        "language": payload.language,
        "explanation": explanation,
        "audio_format": payload.audio_format or "unknown",
        "processing_time_ms": processing_time
    }


@app.get("/")
def root():
    return {
        "status": "running",
        "service": "AI Voice Detector API",
        "health": "OK"
    }
