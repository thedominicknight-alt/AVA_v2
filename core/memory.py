import json
import os
from datetime import datetime

DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'memory_logs.json')

def store_possibilities(chosen_branch, rejected_branches, gpt_response=None):
    print("[Memory] Storing possibilities.")
    log_entry = {
        'timestamp': datetime.now().isoformat(),
        'chosen_branch': chosen_branch,
        'gpt_response': gpt_response,
        'rejected_branches': [b for b in rejected_branches if b['path_id'] != chosen_branch['path_id']]
    }

    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
    if not os.path.exists(DATA_PATH):
        with open(DATA_PATH, 'w') as f:
            json.dump([], f)

    with open(DATA_PATH, 'r+') as f:
        data = json.load(f)
        data.append(log_entry)
        f.seek(0)
        json.dump(data, f, indent=4)

    print(f"[Memory] Log saved. Total entries: {len(data)}")


def recall_memory():
    print("[Memory] Recalling memory...")
    if not os.path.exists(DATA_PATH):
        return "I have no memory logs yet."

    with open(DATA_PATH, 'r') as f:
        data = json.load(f)

    if not data:
        return "My memory is currently empty."

    summary = []
    for i, entry in enumerate(data):
        timestamp = entry['timestamp']
        chosen = entry['chosen_branch']['simulation']
        gpt_reply = entry.get('gpt_response', 'No detailed explanation saved.')
        summary.append(f"{i+1}. [{timestamp}] - {chosen}\n{gpt_reply}\n")

    return "Here’s what I remember:\n" + "\n".join(summary)
def search_memory(keyword):
    print(f"[Memory] Searching memory for keyword: {keyword}")
    if not os.path.exists(DATA_PATH):
        return "I have no memory logs yet."

    with open(DATA_PATH, 'r') as f:
        data = json.load(f)

    keyword = keyword.lower()
    matches = []

    for i, entry in enumerate(data):
        text = entry.get('gpt_response', '') or ''
        if keyword in text.lower():
            timestamp = entry['timestamp']
            topic = entry['chosen_branch']['simulation']
            matches.append(f"{i+1}. [{timestamp}] - {topic}\n{text.strip()}\n")

    if not matches:
        return "I found nothing in my memory matching that keyword."

    return "Here's what I found:\n\n" + "\n".join(matches)
