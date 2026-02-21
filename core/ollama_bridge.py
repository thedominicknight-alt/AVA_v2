import urllib.request
import json

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen2:0.5b"

def ask_ollama(prompt: str) -> str:
    payload = {
        "model": MODEL,
        "prompt": f"<|system|>You are AVA. Reply in ONE short sentence only.</s><|user|>{prompt}</s><|assistant|>",
        "stream": False,
        "options": {
            "temperature": 0.7,
            "num_predict": 40,
            "stop": ["</s>", "<|user|>", ".", "!"]
        }
    }

    try:
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            OLLAMA_URL,
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=120) as response:
            result = json.loads(response.read().decode("utf-8"))
            response_text = result.get("response", "").strip()
            # Hard truncate to first sentence
            for punct in [".", "!", "?"]:
                if punct in response_text:
                    response_text = response_text.split(punct)[0] + punct
                    break
            return response_text

    except Exception as e:
        print(f"[Ollama] Error: {e}")
        return "I'm having trouble thinking right now."
