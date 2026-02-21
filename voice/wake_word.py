import pvporcupine
import sounddevice as sd
import numpy as np

WAKE_WORD = "jarvis"
MIC_DEVICE = 1
MIC_RATE = 44100

def wait_for_wake_word(access_key: str) -> bool:
    """Blocks until wake word is detected. Returns True when heard."""
    porcupine = pvporcupine.create(access_key=access_key, keywords=[WAKE_WORD])
    
    pico_rate = porcupine.sample_rate  # 16000
    frame_len = porcupine.frame_length
    # How many 44100Hz samples we need to produce one 16000Hz frame
    read_len = int(frame_len * MIC_RATE / pico_rate)

    print(f"[WakeWord] Listening for '{WAKE_WORD}'...")

    try:
        with sd.RawInputStream(samplerate=MIC_RATE,
                               channels=1,
                               dtype='int16',
                               blocksize=read_len,
                               device=MIC_DEVICE) as stream:
            while True:
                pcm, _ = stream.read(read_len)
                pcm = np.frombuffer(pcm, dtype=np.int16)
                # Downsample from 44100 to 16000
                indices = np.round(np.linspace(0, len(pcm)-1, frame_len)).astype(int)
                pcm = pcm[indices].tolist()
                result = porcupine.process(pcm)
                if result >= 0:
                    print("[WakeWord] Wake word detected!")
                    return True
    finally:
        porcupine.delete()
