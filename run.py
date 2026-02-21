"""
AVA - Adaptive Voice Assistant
Main entry point. Run this on your Raspberry Pi.
"""

from engine.main_loop import ava_core_loop
from voice.listener import listen_for_wake_word, transcribe_speech
from voice.speaker import speak
import time

WAKE_WORD = "ava"

def main():
    speak("AVA is online. Say 'AVA' to wake me.")
    print("[AVA] System ready. Listening for wake word...")

    while True:
        try:
            # Wait for wake word
            if listen_for_wake_word(WAKE_WORD):
                speak("Yes?")
                print("[AVA] Wake word detected. Listening for command...")

                # Transcribe what the user says
                user_input = transcribe_speech()

                if not user_input:
                    speak("I didn't catch that. Please try again.")
                    continue

                print(f"[AVA] You said: {user_input}")

                # Run through AVA's brain
                response = ava_core_loop(user_input)

                # Speak the response
                print(f"[AVA] Response: {response}")
                speak(response)

        except KeyboardInterrupt:
            speak("Shutting down. Goodbye.")
            print("[AVA] Shutdown requested.")
            break
        except Exception as e:
            print(f"[AVA] Error in main loop: {e}")
            time.sleep(1)

if __name__ == "__main__":
    main()
