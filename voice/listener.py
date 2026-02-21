import sounddevice as sd
import numpy as np
import vosk
import json

MODEL_PATH = "/home/pi/AVA_v2/data/vosk-model"
SAMPLE_RATE = 44100

_model = None

def load_model():
    global _model
    if _model is None:
        print("[Listener] Loading Vosk model...")
        _model = vosk.Model(MODEL_PATH)
        print("[Listener] Ready.")
    return _model

def listen(seconds=5) -> str:
    model = load_model()
    rec = vosk.KaldiRecognizer(model, SAMPLE_RATE)
    print(f"[Listener] Recording {seconds} seconds - speak now...")
    audio = sd.rec(int(seconds * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1, device=None)
    sd.wait()
    audio_bytes = (audio * 32767).astype(np.int16).tobytes()
    rec.AcceptWaveform(audio_bytes)
    result = json.loads(rec.FinalResult())
    text = result.get("text", "").strip()
    print(f"[Listener] Heard: {text}")
    return text
