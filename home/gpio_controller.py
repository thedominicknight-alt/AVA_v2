try:
    import RPi.GPIO as GPIO
    GPIO_AVAILABLE = True
except ImportError:
    GPIO_AVAILABLE = False
    print("[GPIO] WARNING: RPi.GPIO not found. Running in simulation mode.")

PIN_LIGHTS = 12
PIN_RELAY = 17
PIN_PIR = 27

class GPIOController:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self.pwm = None
        self.current_brightness = 100

        if GPIO_AVAILABLE:
            GPIO.cleanup()
            GPIO.setmode(GPIO.BCM)
            GPIO.setwarnings(False)
            GPIO.setup(PIN_LIGHTS, GPIO.OUT)
            GPIO.setup(PIN_RELAY, GPIO.OUT)
            GPIO.setup(PIN_PIR, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
            self.pwm = GPIO.PWM(PIN_LIGHTS, 1000)
            self.pwm.start(0)
            print("[GPIO] Initialized successfully.")
        else:
            print("[GPIO] Simulation mode active.")

    def set_light(self, state: bool):
        self.set_light_brightness(100 if state else 0)

    def set_light_brightness(self, percent: int):
        percent = max(0, min(100, percent))
        self.current_brightness = percent
        if GPIO_AVAILABLE and self.pwm:
            self.pwm.ChangeDutyCycle(percent)
            print(f"[GPIO] Light brightness set to {percent}%")
        else:
            print(f"[GPIO] SIMULATED: Light brightness → {percent}%")

    def set_relay(self, state: bool):
        if GPIO_AVAILABLE:
            GPIO.output(PIN_RELAY, GPIO.HIGH if state else GPIO.LOW)
            print(f"[GPIO] Relay set to {'ON' if state else 'OFF'}")
        else:
            print(f"[GPIO] SIMULATED: Relay → {'ON' if state else 'OFF'}")

    def read_pir(self) -> bool:
        if GPIO_AVAILABLE:
            return GPIO.input(PIN_PIR) == GPIO.HIGH
        return False

    def cleanup(self):
        if GPIO_AVAILABLE:
            if self.pwm:
                self.pwm.stop()
            GPIO.cleanup()
            print("[GPIO] Cleaned up.")
