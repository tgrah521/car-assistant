import json
import subprocess
import os
import time
from voice import say, recognize_text


def send_message():
    say("An wen möchten Sie eine Nachricht senden?")
    kontakt_name = recognize_text().strip().lower()

    try:
        with open("/home/tgrah/kontakte.json", "r") as f:
            kontakte = json.load(f)
    except FileNotFoundError:
        say("Kontakte-Datei nicht gefunden.")
        return

    if kontakt_name not in kontakte:
        say(f"Ich konnte keinen Kontakt namens {kontakt_name} finden.")
        return

    empfänger = kontakte[kontakt_name]

    say("Wie lautet die Nachricht?")
    message = recognize_text()

    say(f"Ich sende '{message}' an {kontakt_name}. Ist das korrekt?")
    confirmation = recognize_text().lower()

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
    file_path = "/home/tgrah/my-whatsapp-bot/nachrichten.json"
    
    if not os.path.exists(file_path):
        print("Datei existiert nicht!")
        return

    last_modified = os.path.getmtime(file_path)
    print("Now detecting filechanges")

    while True:
        try:
            current_modified = os.path.getmtime(file_path)
            if current_modified != last_modified:
                print("File has changed!")
                last_modified = current_modified
        except FileNotFoundError:
            print("Datei wurde gelöscht oder verschoben.")
        time.sleep(2)

