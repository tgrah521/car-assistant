import speech_recognition as sr
import RPi.GPIO as GPIO
import pyttsx3
from audio_player import stream_and_download, play_mp3
from load_songs import get_random_song
from whatsapp import send_message
from ai import ask_question

BUTTON_PIN = 17  
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def say(text):
    engine = pyttsx3.init()
    engine.getProperty('voices')

    engine.setProperty('pitch', 40)
    engine.setProperty('rate', 130)
    engine.setProperty('voice','german')
    engine.setProperty('text','normalize')
    engine.say(text)
    engine.runAndWait()

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
                audio = recognizer.listen(source,timeout=2, phrase_time_limit=3) 
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

def recognize_text():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source,timeout=2, phrase_time_limit=3) 
                # Spracherkennung
            return recognizer.recognize_google(audio, language="de-DE")
        except sr.WaitTimeoutError as e:
            return ""
        except sr.UnknownValueError:
            return ""
        except KeyboardInterrupt:
            return ""
            
def handle_voice_command():
    while True:
        if listen():
            play_mp3("/home/tgrah/Dokumente/hearing.mp3",2)
            action = recognize_text()
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
                    stream_and_download(song,".")
                elif "frage" in action.lower():
                    ask_question()
                elif "spiele" in action.lower():
                    stream_and_download(action.lower().split("spiele", 1)[1].strip(), ".")
                