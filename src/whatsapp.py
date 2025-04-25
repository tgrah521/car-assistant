import json
import subprocess
import os
import time
from voice import say, recognize_text
from audio_player import play_mp3

CONTACTS_FILE = os.path.join(os.path.dirname(__file__), '../resource/kontakte.json')
MESSAGES_FILE = os.path.join(os.path.dirname(__file__), '../resource/nachrichten.json')

def send_message():
    kontakt_name = recognize_text("An wen möchten Sie eine Nachricht senden?").strip().lower()

    try:
        with open(CONTACTS_FILE, "r") as f:
            kontakte = json.load(f)
    except FileNotFoundError:
        say("Kontakte-Datei nicht gefunden.")
        return

    if kontakt_name not in kontakte:
        say(f"Ich konnte keinen Kontakt namens {kontakt_name} finden.")
        return

    empfänger = kontakte[kontakt_name]

    message = recognize_text("Wie lautet die Nachricht?")

    say(f"Ich sende '{message}' an {kontakt_name}. Ist das korrekt?")
    confirmation = recognize_text("").lower()

    if confirmation in ["ja", "korrekt", "stimmt", "richtig"]:
        command = ["npx", "mudslide", "send", empfänger, message]
        try:
            result = subprocess.run(command, check=True, capture_output=True, text=True)
            say("Nachricht wurde gesendet.")
            print("Nachricht gesendet!")
            print(result.stdout)
        except subprocess.CalledProcessError as e:
            say("Es gab ein Problem beim Senden der Nachricht.")
            print("Fehler beim Senden:")
            print(e.stderr)
    else:
        send_message()



def check_for_messages():
    if not os.path.exists(MESSAGES_FILE):
        print("Datei existiert nicht!")
        return

    last_modified = os.path.getmtime(MESSAGES_FILE)
    print("Now detecting filechanges")

    while True:
        try:
            print("checking...")
            current_modified = os.path.getmtime(MESSAGES_FILE)
            if current_modified != last_modified:
                print("File has changed!")
                say(f"Sie haben eine neue nachricht!")
                confirmation = recognize_text("Soll ich sie vorlesen?").lower()

                if confirmation in ["ja", "korrekt", "stimmt", "richtig"]:
                    with open(MESSAGES_FILE, "r", encoding="utf-8") as f:
                        nachrichten = json.load(f)
                        if nachrichten:
                            letzte_nachricht = nachrichten[-1]
                            absender = letzte_nachricht.get("von", "Unbekannt")
                            text = letzte_nachricht.get("text", "Kein Text")
                            nachricht_typ = letzte_nachricht.get("type", "unbekannt")

                            if nachricht_typ == "chat":
                                say(f"{absender} schrieb")
                                say(text)
                                print(f"{absender} schrieb")
                                print(text)
                            else:
                                say(f"{absender} sendet")
                                say(f"{nachricht_typ}")

                last_modified = current_modified
        except FileNotFoundError:
            print("Datei wurde gelöscht oder verschoben.")
        time.sleep(2)