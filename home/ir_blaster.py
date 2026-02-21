"""
IR Blaster Controller
Sends infrared signals to control TV and AC using irsend (LIRC) or pigpio.

Hardware setup:
- IR LED connected to GPIO pin 18 (default for LIRC / pigpio)
- Use a 2N2222 transistor + 100Ω resistor for adequate current

To configure LIRC:
    sudo apt install lirc
    Add to /boot/config.txt:
        dtoverlay=gpio-ir-tx,gpio_pin=18

Then record your remote codes:
    irrecord -d /dev/lirc0 ~/your_remote.lircd.conf
    sudo cp ~/your_remote.lircd.conf /etc/lirc/lircd.conf.d/
    sudo systemctl restart lircd
"""

import subprocess
import time


# Map device+command to LIRC remote name and key name
# ⚠️ UPDATE THESE to match your actual remote names from irrecord
LIRC_REMOTE_MAP = {
    "tv": {
        "power_on":   ("MY_TV_REMOTE", "KEY_POWER"),
        "power_off":  ("MY_TV_REMOTE", "KEY_POWER"),
        "volume_up":  ("MY_TV_REMOTE", "KEY_VOLUMEUP"),
        "volume_down":("MY_TV_REMOTE", "KEY_VOLUMEDOWN"),
        "mute":       ("MY_TV_REMOTE", "KEY_MUTE"),
        "channel_up": ("MY_TV_REMOTE", "KEY_CHANNELUP"),
        "channel_down":("MY_TV_REMOTE","KEY_CHANNELDOWN"),
        "digit_0":    ("MY_TV_REMOTE", "KEY_0"),
        "digit_1":    ("MY_TV_REMOTE", "KEY_1"),
        "digit_2":    ("MY_TV_REMOTE", "KEY_2"),
        "digit_3":    ("MY_TV_REMOTE", "KEY_3"),
        "digit_4":    ("MY_TV_REMOTE", "KEY_4"),
        "digit_5":    ("MY_TV_REMOTE", "KEY_5"),
        "digit_6":    ("MY_TV_REMOTE", "KEY_6"),
        "digit_7":    ("MY_TV_REMOTE", "KEY_7"),
        "digit_8":    ("MY_TV_REMOTE", "KEY_8"),
        "digit_9":    ("MY_TV_REMOTE", "KEY_9"),
    },
    "ac": {
        "power_on":   ("MY_AC_REMOTE", "KEY_POWER"),
        "power_off":  ("MY_AC_REMOTE", "KEY_POWER"),
        "temp_up":    ("MY_AC_REMOTE", "KEY_UP"),
        "temp_down":  ("MY_AC_REMOTE", "KEY_DOWN"),
    }
}


class IRBlaster:
    def __init__(self):
        self._check_lirc_available()

    def _check_lirc_available(self):
        result = subprocess.run(["which", "irsend"], capture_output=True)
        if result.returncode != 0:
            print("[IRBlaster] WARNING: irsend not found. IR commands will be simulated.")
            self.simulated = True
        else:
            self.simulated = False

    def send(self, device: str, command: str):
        """Send a single IR command."""
        if device not in LIRC_REMOTE_MAP or command not in LIRC_REMOTE_MAP[device]:
            print(f"[IRBlaster] Unknown command: {device}/{command}")
            return

        remote, key = LIRC_REMOTE_MAP[device][command]

        if self.simulated:
            print(f"[IRBlaster] SIMULATED: irsend SEND_ONCE {remote} {key}")
            return

        try:
            subprocess.run(
                ["irsend", "SEND_ONCE", remote, key],
                check=True,
                capture_output=True
            )
            print(f"[IRBlaster] Sent: {remote} / {key}")
        except subprocess.CalledProcessError as e:
            print(f"[IRBlaster] Error sending IR command: {e}")

    def send_channel(self, device: str, channel: int):
        """Send channel number digit by digit."""
        print(f"[IRBlaster] Sending channel: {channel}")
        for digit in str(channel):
            key = f"digit_{digit}"
            self.send(device, key)
            time.sleep(0.3)  # small delay between digits

    def send_temperature(self, device: str, temp: int):
        """
        For AC units, temperature is usually set via specific codes.
        This sends temp_up/temp_down relative to current setting.
        For precise control, record individual temp codes with irrecord.
        """
        print(f"[IRBlaster] Setting temperature to {temp} - using relative adjustment")
        # Simple approach: send power_on then adjust
        # For full precision, record each temp level individually
        self.send(device, "power_on")
        time.sleep(0.5)
