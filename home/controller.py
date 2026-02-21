"""
Home Controller
Routes home control commands to the correct hardware interface (IR blaster or GPIO).
"""

from home.ir_blaster import IRBlaster
from home.gpio_controller import GPIOController
from home.sensors import SensorManager

ir = IRBlaster()
gpio = GPIOController()
sensors = SensorManager()


def execute_home_command(intent: dict) -> str:
    """
    Takes a classified home control intent and executes the appropriate hardware command.
    Returns a human-readable confirmation string for AVA to speak.
    """
    device = intent.get("device", "unknown")
    action = intent.get("action", "")
    value = intent.get("value")
    raw = intent.get("raw", "")

    print(f"[HomeController] Device={device}, Action={action}, Value={value}")

    try:
        # --- TV ---
        if device == "tv":
            if action == "turn_on":
                ir.send("tv", "power_on")
                return "Turning the TV on."
            elif action == "turn_off":
                ir.send("tv", "power_off")
                return "Turning the TV off."
            elif action == "change_channel" and value is not None:
                ir.send_channel("tv", value)
                return f"Switching to channel {value}."
            elif action == "increase":
                ir.send("tv", "volume_up")
                return "Volume up."
            elif action == "decrease":
                ir.send("tv", "volume_down")
                return "Volume down."
            elif action == "mute":
                ir.send("tv", "mute")
                return "TV muted."
            elif action == "unmute":
                ir.send("tv", "mute")  # most TVs toggle mute
                return "TV unmuted."
            else:
                return "I'm not sure what to do with the TV. Try saying turn on, turn off, or change channel."

        # --- AC / Thermostat ---
        elif device == "ac":
            if action == "turn_on":
                ir.send("ac", "power_on")
                return "Turning the AC on."
            elif action == "turn_off":
                ir.send("ac", "power_off")
                return "Turning the AC off."
            elif action in ["increase", "set"] and value is not None:
                ir.send_temperature("ac", value)
                return f"Setting AC temperature to {value} degrees."
            elif action == "increase":
                ir.send("ac", "temp_up")
                return "Increasing AC temperature."
            elif action == "decrease":
                ir.send("ac", "temp_down")
                return "Decreasing AC temperature."
            else:
                return "I can turn the AC on, off, or adjust the temperature."

        # --- Lights ---
        elif device == "lights":
            if action in ["turn_on", "brighten"]:
                gpio.set_light(True)
                return "Lights on."
            elif action == "turn_off":
                gpio.set_light(False)
                return "Lights off."
            elif action == "dim":
                level = value if value else 30  # default 30% brightness
                gpio.set_light_brightness(level)
                return f"Dimming lights to {level} percent."
            elif action == "set" and value is not None:
                gpio.set_light_brightness(value)
                return f"Setting lights to {value} percent."
            else:
                return "I can turn the lights on, off, or dim them."

        # --- Sensor status ---
        elif action == "status" or "check" in raw:
            return sensors.get_status_report()

        # --- Generic appliance (GPIO relay) ---
        elif device == "appliance":
            if action in ["turn_on", "switch_on"]:
                gpio.set_relay(True)
                return "Appliance turned on."
            elif action in ["turn_off", "switch_off"]:
                gpio.set_relay(False)
                return "Appliance turned off."

        return f"I'm not sure how to handle that command. You said: {raw}"

    except Exception as e:
        print(f"[HomeController] Error executing command: {e}")
        return "I had trouble executing that command. Please check the hardware connections."
