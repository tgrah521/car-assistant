import speech_recognition as sr
#import RPi.GPIO as GPIO
import threading
import sounddevice
import os
from whatsapp import check_for_messages
from audio_player import stream_and_download, start_auto_play
from load_songs import get_random_song
from whatsapp import send_message
from ai import ask_question
from voice import say, recognize_text
from obd_commands import say_obd_command
from models.voice_commands_enums import VoiceCommand
from help import tell_all_voice_commands
from network import check_for_connection, get_ip_adress
from vlc_manager import close_all_vlc
from playlist import playlist_add, playlist_remove, playlist_clear, playlist_start, playlist_save, playlist_load, playlist_delete, playlist_list
from radio import start_radio_thread
KOPIEREN = False
BUTTON_PIN = 17
#GPIO.setmode(GPIO.BCM)
#GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

HEARING_MP3 = os.path.join(os.path.dirname(__file__), '../resource/hearing.mp3')

def listen():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    while True:
        with microphone as source:
            recognizer.adjust_for_ambient_noise(source)
            print("Hört zu...")
            try:
                check_for_connection()
   #             if GPIO.input(BUTTON_PIN) == GPIO.LOW:
   #                 return True
                audio = recognizer.listen(source,timeout=3, phrase_time_limit=3)
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
    global KOPIEREN
    # Currently disabled because no method for recieving Whatsapp Messages and writing in "nachrichten.json"
    # threading.Thread(target=check_for_messages).start()

    while True:
        if listen():
            close_all_vlc()
            #play_mp3(HEARING_MP3, 2)
            action = recognize_text("ja?")
            if "1X" in action:
                action = action.replace('1X ', '')
                action = recognize_text(f"{action}. Bitte Wiederhole")

            command = VoiceCommand.from_text(action)
            if command is None:
                say("Das habe ich leider nicht verstanden")
            else:
                if command == VoiceCommand.WHATSAPP:
                    send_message()
                elif command == VoiceCommand.MUSIK:
                    song = get_random_song()
                    if song == "":
                        say("Deine Liste scheint leer zu sein")
                        continue
                    stream_and_download(song, ".", KOPIEREN)
                elif command == VoiceCommand.LOOP:
                    start_auto_play(KOPIEREN)
                elif command == VoiceCommand.FRAGE:
                    ask_question()
                elif command == VoiceCommand.TANK:
                    say_obd_command("FUEL_LEVEL")
                elif command == VoiceCommand.KUEHLWASSER:
                    say_obd_command("COOLANT_TEMP")
                elif command == VoiceCommand.BATTERIE:
                    say_obd_command("CONTROL_MODULE_VOLTAGE")
                elif command == VoiceCommand.KOPIEREN:
                    KOPIEREN = not KOPIEREN
                    if KOPIEREN:
                        say("Kopieren wurde aktiviert")
                    else:
                        say("Kopieren wurde deaktiviert")
                elif command == VoiceCommand.HELP:
                    tell_all_voice_commands()
                elif command == VoiceCommand.SPIELE:
                    stream_and_download(action.lower().split("spiele", 1)[1].strip(), ".", KOPIEREN)
                elif command == VoiceCommand.PLAYLIST_ADD:
                    playlist_add()
                elif command == VoiceCommand.PLAYLIST_CLEAR:
                    playlist_clear()
                elif command == VoiceCommand.PLAYLIST_REMOVE:
                    playlist_remove()
                elif command == VoiceCommand.PLAYLIST_PLAY:
                    playlist_start(KOPIEREN)
                elif command == VoiceCommand.PLAYLIST_SAVE:
                    playlist_save()
                elif command == VoiceCommand.PLAYLIST_LOAD:
                    playlist_load()
                elif command == VoiceCommand.PLAYLIST_DELETE:
                    playlist_delete()
                elif command == VoiceCommand.PLAYLIST_LIST:
                    playlist_list()
                elif command == VoiceCommand.EXIT:
                    say("Aufwiedersehen")
                    exit()
                elif command == VoiceCommand.RADIO:
                    start_radio_thread()
                elif command == VoiceCommand.IP_ADRESS:
                    get_ip_adress()
                
            