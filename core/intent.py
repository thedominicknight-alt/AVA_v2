"""
Intent Classifier
Determines whether the user wants to control a home device or have a conversation.
This runs BEFORE hitting the AI model, keeping home commands fast and reliable.
"""

# Keywords that indicate home control commands
HOME_CONTROL_TRIGGERS = {
    # Lights
    "light": "lights",
    "lights": "lights",
    "lamp": "lights",
    "bright": "lights",
    "dim": "lights",

    # TV
    "tv": "tv",
    "television": "tv",
    "channel": "tv",
    "volume": "tv",
    "stream": "tv",
    "netflix": "tv",
    "youtube": "tv",

    # AC / Thermostat
    "ac": "ac",
    "air con": "ac",
    "air conditioning": "ac",
    "fan": "ac",
    "temperature": "ac",
    "thermostat": "ac",
    "cool": "ac",
    "heat": "ac",
    "warm": "ac",

    # General appliances
    "turn on": "appliance",
    "turn off": "appliance",
    "switch on": "appliance",
    "switch off": "appliance",
    "plug": "appliance",
    "socket": "appliance",
}

# Action keywords
ACTION_KEYWORDS = {
    "on": "turn_on",
    "off": "turn_off",
    "turn on": "turn_on",
    "turn off": "turn_off",
    "switch on": "turn_on",
    "switch off": "turn_off",
    "increase": "increase",
    "decrease": "decrease",
    "up": "increase",
    "down": "decrease",
    "higher": "increase",
    "lower": "decrease",
    "channel": "change_channel",
    "mute": "mute",
    "unmute": "unmute",
    "dim": "dim",
    "brighten": "brighten",
    "set": "set",
    "status": "status",
    "check": "status",
}


def classify_intent(parsed_input: dict) -> dict:
    """
    Returns an intent dict like:
    {
        "type": "home_control",
        "device": "lights",
        "action": "turn_on",
        "value": None,
        "raw": "turn on the lights"
    }
    or
    {
        "type": "conversation",
        "raw": "what is quantum computing"
    }
    """
    text = parsed_input.get("parsed_text", "").lower()

    detected_device = None
    detected_action = None
    detected_value = None

    # Check for device mentions
    for keyword, device in HOME_CONTROL_TRIGGERS.items():
        if keyword in text:
            detected_device = device
            break

    # Check for action keywords
    for keyword, action in ACTION_KEYWORDS.items():
        if keyword in text:
            detected_action = action
            break

    # Try to extract a numeric value (e.g. "channel 5", "volume 30", "22 degrees")
    import re
    numbers = re.findall(r'\b\d+\b', text)
    if numbers:
        detected_value = int(numbers[0])

    # If we found a device or a clear control action, it's a home control intent
    if detected_device or (detected_action in ["turn_on", "turn_off", "switch_on", "switch_off"]):
        return {
            "type": "home_control",
            "device": detected_device or "unknown",
            "action": detected_action or "turn_on",
            "value": detected_value,
            "raw": text
        }

    # Otherwise it's a conversation
    return {
        "type": "conversation",
        "raw": text
    }


# Simple questions that should bypass deep reasoning
SIMPLE_TRIGGERS = [
    "what time", "what's the time", "what date", "what day",
    "tell me a joke", "say hello", "who are you", "what are you",
    "how are you", "what is your name", "your name"
]

def is_simple_question(text: str) -> bool:
    text = text.lower()
    return any(trigger in text for trigger in SIMPLE_TRIGGERS)


# Simple questions that should bypass deep reasoning
SIMPLE_TRIGGERS = [
    "what time", "what's the time", "what date", "what day",
    "tell me a joke", "say hello", "who are you", "what are you",
    "how are you", "what is your name", "your name"
]

def is_simple_question(text: str) -> bool:
    text = text.lower()
    return any(trigger in text for trigger in SIMPLE_TRIGGERS)
