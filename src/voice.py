import pyttsx3
import speech_recognition as sr

def say(text):
    engine = pyttsx3.init()
    engine.getProperty('voices')

    engine.setProperty('pitch', 40)
    engine.setProperty('rate', 130)
    engine.setProperty('voice','german')
    engine.setProperty('text','normalize')
    engine.say(text)
    engine.runAndWait()

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