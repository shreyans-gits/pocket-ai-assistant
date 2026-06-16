import speech_recognition as sr
import pygame
import os
import tempfile
import asyncio
import edge_tts
import threading


class Voice:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.recognizer.pause_threshold = 1
        self.audio_lock = threading.Lock()
        self.voice_name = "en-US-GuyNeural"

    def speak(self, text: str):
        # print(f"ZORO: {text}")

        async def generate():
            temp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
            temp.close()

            communicate = edge_tts.Communicate(text=text, voice=self.voice_name)
            await communicate.save(temp.name)
            return temp.name

        with self.audio_lock:
            try:
                file_path = asyncio.run(generate())

                pygame.mixer.init()
                pygame.mixer.music.load(file_path)
                pygame.mixer.music.play()

                while pygame.mixer.music.get_busy():
                    pygame.time.Clock().tick(10)

                pygame.mixer.quit()

                try:
                    os.remove(file_path)
                except Exception as e:
                    print(f"[Voice Cleanup Warning] Could not remove temp file: {e}")

            except Exception as e:
                print("Speak error:", e)

    def listen(self) -> str:
        try:
            with sr.Microphone() as source:
                print("Adjusting noise...")
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)

                print("Listening...")
                audio = self.recognizer.listen(source, timeout=5)

            print("Recognizing...")
            query = self.recognizer.recognize_google(audio)
            # print("You:", query)
            return query

        except sr.WaitTimeoutError:
            print("You didn't say anything")
            return ""
        except sr.UnknownValueError:
            return ""
        except sr.RequestError as e:
            print("Google STT error:", e)
            return ""
        except Exception as e:
            print("Error:", e)
            return ""