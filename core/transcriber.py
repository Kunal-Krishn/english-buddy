import whisper
import os

model = whisper.load_model("base")

def transcribe_audio(audio_path: str) -> str:
    """Transcribe audio file using Whisper base model."""
    try:
        print(f"Transcribing file: {audio_path}")
        print(f"File exists: {os.path.exists(audio_path)}")
        print(f"File size: {os.path.getsize(audio_path)} bytes")
        
        result = model.transcribe(audio_path, fp16=False)
        transcript = result["text"].strip()
        
        print(f"Transcript: {transcript}")
        return transcript
    except Exception as e:
        print(f"Transcription error: {e}")
        import traceback
        traceback.print_exc()
        return ""