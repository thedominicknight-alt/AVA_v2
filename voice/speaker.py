import subprocess
import os

PIPER_PATH = os.path.expanduser("~/piper/piper")
VOICE_MODEL = os.path.expanduser("~/piper/en_US-ljspeech-medium.onnx")

_piper_available = os.path.exists(os.path.expanduser(PIPER_PATH)) and os.path.exists(os.path.expanduser(VOICE_MODEL))

if _piper_available:
    print("[Speaker] Piper TTS ready.")
else:
    print("[Speaker] Piper not found. Falling back to espeak.")

def speak(text: str):
    if not text:
        return
    print(f"[Speaker] Speaking: {text}")
    if _piper_available:
        _speak_piper(text)
    else:
        _speak_espeak(text)

def _speak_piper(text: str):
    try:
        safe_text = text.replace("'", "'\\''")
        piper_cmd = f"echo '{safe_text}' | {PIPER_PATH} --model {VOICE_MODEL} --output_raw | aplay -r 22050 -f S16_LE -c 1 -D hw:0,0"
        subprocess.run(piper_cmd, shell=True, check=True, stderr=subprocess.DEVNULL)
    except Exception as e:
        print(f"[Speaker] Piper error: {e}")
        _speak_espeak(text)

def _speak_espeak(text: str):
    try:
        subprocess.run(["espeak", text], check=True)
    except Exception as e:
        print(f"[Speaker] espeak error: {e}")
