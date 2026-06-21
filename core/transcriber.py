import whisper
import os

model = whisper.load_model("base")

def transcribe_audio(audio_path: str) -> str:
    """Transcribe audio file using Whisper base model."""
    try:
        result = model.transcribe(audio_path)
        return result["text"].strip()
    except Exception as e:
        print(f"Transcription error: {e}")
        return ""
