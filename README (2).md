# AVA — Offline AI Smart Home Assistant

> A fully private, offline AI assistant that runs entirely on a Raspberry Pi 4. No cloud. No subscriptions. No data leaves your home.

![Raspberry Pi](https://img.shields.io/badge/Raspberry%20Pi-4-red?logo=raspberrypi) ![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python) ![License](https://img.shields.io/badge/License-MIT-green) ![Status](https://img.shields.io/badge/Status-Active-brightgreen)

---

## What is AVA?

AVA (Autonomous Voice Assistant) is a smart home AI assistant that runs completely offline on a Raspberry Pi 4. Unlike Alexa, Google Home, or Siri — AVA never connects to the cloud. Every word you say stays on your device.

AVA listens, thinks, and speaks — all locally. She controls your home, answers questions, learns from conversations, and gets smarter over time.

**Why this matters:** Most AI assistants require internet access and send your voice data to remote servers. AVA proves this doesn't have to be the case. Powerful AI can run privately on £50 of hardware.

---

## Features

- 🎙️ **Voice Input** — Offline speech recognition via Vosk (ARM-optimised)
- 🔊 **Natural Voice Output** — High-quality TTS via Piper
- 🧠 **Local AI Brain** — Powered by Ollama + Qwen2 running fully on-device
- 🏠 **Smart Home Control** — Controls lights, relays, and GPIO devices
- 📡 **IR Transmitter** — Send IR signals to control TVs and appliances
- 🧬 **Reasoning Engine** — Multi-branch thought simulation with reflection
- 💾 **Persistent Memory** — Learns from every conversation
- 🔒 **100% Offline** — Zero cloud dependency, zero data collection

---

## Hardware Requirements

| Component | Details |
|-----------|---------|
| Raspberry Pi 4 | 4GB RAM recommended |
| USB Microphone | Any USB mic works |
| Speaker | 3.5mm headphone jack or Bluetooth |
| IR Receiver Module | V1222 (GPIO 17) — optional |
| IR Transmitter Module | V1221 (GPIO 18) — optional |

---

## Architecture

```
You speak
    ↓
[Vosk] Speech Recognition (offline, ARM-native)
    ↓
[Intent Classifier] Home control vs conversation
    ↓
[Reasoning Engine] Multi-branch thought simulation
    ↓
[Ollama / Qwen2] Local language model response
    ↓
[Piper TTS] Natural voice synthesis
    ↓
AVA speaks
```

AVA's reasoning engine simulates multiple response branches, scores them, selects the best, and learns which thinking patterns work best over time — all without internet access.

---

## Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/AVA_v2.git
cd AVA_v2
```

### 2. Install dependencies

```bash
pip install vosk sounddevice numpy RPi.GPIO --break-system-packages
sudo apt install espeak
```

### 3. Install Ollama and download the AI model

```bash
curl -fsSL https://ollama.ai/install.sh | sh
ollama pull qwen2:0.5b
```

### 4. Install Piper TTS

```bash
cd ~ && wget https://github.com/rhasspy/piper/releases/download/v1.2.0/piper_arm64.tar.gz
tar -xzf piper_arm64.tar.gz
mkdir -p ~/piper && mv piper ~/piper/bin
wget -P ~/piper/ https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/ljspeech/medium/en_US-ljspeech-medium.onnx
wget -P ~/piper/ https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/ljspeech/medium/en_US-ljspeech-medium.onnx.json
```

### 5. Download the Vosk speech recognition model

```bash
cd ~ && wget https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip
unzip vosk-model-small-en-us-0.15.zip
mv vosk-model-small-en-us-0.15 ~/AVA_v2/data/vosk-model
```

### 6. Run AVA

```bash
cd ~/AVA_v2 && python3 run_voice.py
```

AVA will greet you and start listening.

---

## GPIO Wiring

### IR Receiver (V1222)
```
VCC  → Pin 4  (Row 2, front)
GND  → Pin 9  (Row 5, back)
OUT  → Pin 11 (Row 6, back) — GPIO 17
```

### IR Transmitter (V1221)
```
VCC  → Pin 2  (Row 1, front)
GND  → Pin 6  (Row 3, front)
DAT  → Pin 12 (Row 6, front) — GPIO 18
```

Add to `/boot/firmware/config.txt`:
```
dtoverlay=gpio-ir-tx,gpio_pin=18
dtoverlay=gpio-ir,gpio_pin=17
```

---

## Project Structure

```
AVA_v2/
├── run_voice.py          # Main voice loop entry point
├── engine/
│   └── main_loop.py      # Core reasoning loop
├── core/
│   ├── intent.py         # Intent classification
│   ├── branching.py      # Multi-branch thought simulation
│   ├── reflection.py     # Branch scoring and selection
│   ├── memory.py         # Persistent memory system
│   ├── learning.py       # Pattern learning engine
│   └── ollama_bridge.py  # Local LLM interface
├── voice/
│   ├── listener.py       # Vosk speech recognition
│   └── speaker.py        # Piper TTS
├── home/
│   ├── controller.py     # Home device control
│   ├── gpio_controller.py # GPIO singleton
│   └── sensors.py        # Sensor management
└── data/
    ├── memory_logs.json  # Conversation memory
    └── vosk-model/       # Speech recognition model
```

---

## Privacy

AVA is built on a core principle: **your voice never leaves your home**.

- No API keys required
- No internet connection needed after setup
- No telemetry or usage tracking
- All AI processing happens on your Raspberry Pi

---

## Roadmap

- [ ] Wake word detection ("Hey AVA")
- [ ] Behaviour learning and routine detection
- [ ] Multi-room support via Pi Zero nodes
- [ ] Anomaly detection (unusual sounds, motion patterns)
- [ ] Web dashboard for memory and learning visualisation
- [ ] Home Assistant integration

---

## Contributing

Contributions are welcome. Please open an issue first to discuss what you'd like to change.

---

## License

MIT License — see [LICENSE](LICENSE) for details.

---

## Author

Built by a developer exploring the boundary between privacy, AI, and accessible hardware.

*If this project interests you, give it a ⭐ — it helps others find it.*
