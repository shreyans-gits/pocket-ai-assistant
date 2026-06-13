import speech_recognition as sr
import pyttsx3


class Voice:
    def __init__(self):
        self.recognizer = sr.Recognizer()

        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", 170)

    def listen(self) -> str:
        try:
            with sr.Microphone() as source:
                print("Adjusting noise...")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)

                print("Listening...")
                audio = self.recognizer.listen(source, timeout=5)

            print("Processing...")
            text = self.recognizer.recognize_google(audio)

            return text

        except sr.WaitTimeoutError:
            print("You didn't say anything")
            return ""

        except sr.UnknownValueError:
            print("Could not understand audio")
            return ""

        except sr.RequestError as e:
            print("Google STT error:", e)
            return ""

        except Exception as e:
            print("Error:", e)
            return ""

    def speak(self, text: str):
        try:
            self.engine.say(text)
            self.engine.runAndWait()

        except Exception:
            pass