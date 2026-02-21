from voice.wake_word import wait_for_wake_word
from voice.listener import listen
from voice.speaker import speak
from engine.main_loop import ava_core_loop
import time

ACCESS_KEY = "DVaCIh0cUnksbV1FawCsBJ3vtTbbgGc7UaudP7yVvJZt9cDF27tG4g=="

speak("Hello, I am AVA. Say Jarvis to wake me.")

while True:
    try:
        wait_for_wake_word(ACCESS_KEY)
        speak("Yes?")
        text = listen(5)
        if text and len(text) > 2:
            response = ava_core_loop(text)
            speak(response)
        else:
            speak("I didn't catch that")
        time.sleep(0.3)
    except KeyboardInterrupt:
        speak("Goodbye!")
        break
