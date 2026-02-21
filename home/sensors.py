"""
Sensor Manager
Reads from connected sensors and provides status reports.
Currently supports:
    - PIR motion sensor (GPIO)

Easy to extend: add DHT22, MQ-2 gas sensor, door switches, etc.
"""

from home.gpio_controller import GPIOController
import time
import threading


class SensorManager:
    def __init__(self):
        self.gpio = GPIOController()
        self.motion_detected = False
        self.last_motion_time = None
        self._monitoring = False
        self._monitor_thread = None

    def start_monitoring(self, on_motion_callback=None):
        """
        Start background thread to watch PIR sensor.
        Calls on_motion_callback(event) when motion is detected.
        """
        self._monitoring = True
        self._on_motion = on_motion_callback

        self._monitor_thread = threading.Thread(
            target=self._monitor_loop,
            daemon=True
        )
        self._monitor_thread.start()
        print("[Sensors] Motion monitoring started.")

    def _monitor_loop(self):
        last_state = False
        while self._monitoring:
            current_state = self.gpio.read_pir()

            if current_state and not last_state:
                # Rising edge = motion just detected
                self.motion_detected = True
                self.last_motion_time = time.time()
                print("[Sensors] Motion detected!")

                if self._on_motion:
                    self._on_motion({"type": "motion", "time": self.last_motion_time})

            last_state = current_state
            time.sleep(0.2)  # poll 5x per second

    def stop_monitoring(self):
        self._monitoring = False

    def get_status_report(self) -> str:
        """Returns a spoken status summary of all sensors."""
        lines = []

        # PIR motion
        motion_state = self.gpio.read_pir()
        if motion_state:
            lines.append("Motion is currently being detected.")
        else:
            if self.last_motion_time:
                seconds_ago = int(time.time() - self.last_motion_time)
                lines.append(f"No motion right now. Last detected {seconds_ago} seconds ago.")
            else:
                lines.append("No motion detected since startup.")

        if not lines:
            return "All sensors are reading normally."

        return " ".join(lines)
