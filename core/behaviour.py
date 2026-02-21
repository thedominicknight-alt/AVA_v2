import json
import os
from datetime import datetime
from collections import Counter

BEHAVIOUR_LOG = os.path.expanduser("~/AVA_v2/data/behaviour_log.json")

def _load_log():
    if os.path.exists(BEHAVIOUR_LOG):
        with open(BEHAVIOUR_LOG, "r") as f:
            return json.load(f)
    return []

def _save_log(log):
    os.makedirs(os.path.dirname(BEHAVIOUR_LOG), exist_ok=True)
    with open(BEHAVIOUR_LOG, "w") as f:
        json.dump(log, f, indent=2)

def log_interaction(text, intent_type):
    log = _load_log()
    now = datetime.now()
    log.append({"text": text, "intent": intent_type, "hour": now.hour, "weekday": now.strftime("%A"), "timestamp": now.isoformat()})
    log = log[-500:]
    _save_log(log)

def get_patterns():
    log = _load_log()
    if not log:
        return []
    pattern_keys = [f"{e['weekday']}-{e['hour']}-{e['intent']}" for e in log]
    counts = Counter(pattern_keys)
    return [{"weekday": k.split("-")[0], "hour": int(k.split("-")[1]), "intent": k.split("-")[2], "count": v} for k, v in counts.items() if v >= 3]

def get_proactive_suggestion():
    now = datetime.now()
    for p in get_patterns():
        if p["weekday"] == now.strftime("%A") and p["hour"] == now.hour:
            if p["intent"] == "conversation":
                return "You usually have questions around this time. What is on your mind?"
            elif p["intent"] == "home_control":
                return "You usually adjust something at home around this time. Need anything?"
    return ""
