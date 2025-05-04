import speech_recognition as sr
import RPi.GPIO as GPIO
import threading
import sounddevice
import os
from whatsapp import check_for_messages
from audio_player import stream_and_download, play_mp3
from load_songs import get_random_song
from whatsapp import send_message
from ai import ask_question
from voice import say, recognize_text
from obd_commands import say_obd_command

MUSIK_PROCESS = None
KOPIEREN = False
BUTTON_PIN = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

HEARING_MP3 = os.path.join(os.path.dirname(__file__), '../resource/hearing.mp3')

def listen():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    while True:
        with microphone as source:
            recognizer.adjust_for_ambient_noise(source)
            print("Hört zu...")
            try:
                if GPIO.input(BUTTON_PIN) == GPIO.LOW:
                    return True
                audio = recognizer.listen(source,timeout=3, phrase_time_limit=3)
                # Spracherkennung
                recognized_text = recognizer.recognize_google(audio, language="de-DE")
                print("Erkannter Text:"+ recognized_text)
                if "hallo" in recognized_text.lower() or "hey" in recognized_text.lower() or "bmw" in recognized_text.lower():
                    return True
                else:
                    return False
            except sr.WaitTimeoutError as e:
                pass
            except sr.UnknownValueError:
                return False
            except KeyboardInterrupt:
                return False

def handle_voice_command():
    global MUSIK_PROCESS
    global KOPIEREN
    threading.Thread(target=check_for_messages).start()
    while True:
        if listen():
            if MUSIK_PROCESS:
                MUSIK_PROCESS.terminate()
            #play_mp3(HEARING_MP3, 2)
            action = recognize_text("ja?")
            if action == "":
                say("Das habe ich leider nicht verstanden")
            else:
                if "whatsapp" in action.lower():
                    send_message()
                elif "musik" in action.lower():
                    song = get_random_song()
                    if song == "":
                        say("Deine liste scheint leer zu sein")
                        break
                    MUSIK_PROCESS = stream_and_download(song,".",KOPIEREN)
                elif "frage" in action.lower():
                    ask_question()
                elif "kopieren" in action.lower():
                    KOPIEREN = not KOPIEREN
                    say(KOPIEREN)
                elif "spiele" in action.lower():
                    MUSIK_PROCESS = stream_and_download(action.lower().split("spiele", 1)[1].strip(), ".",KOPIEREN)