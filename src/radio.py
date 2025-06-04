import vlc
import time
import json
import os
import threading
from voice import say, recognize_text

RADIO_STATIONS = os.path.join(os.path.dirname(__file__), '../resource/radio_stations.json')

def start_radio_thread():
    threading.Thread(target=play_radio).start()


def play_radio():
    while True:
        radio_station = recognize_text("Welchen Radiosender möchten Sie hören?").lower()

        if "1X " in radio_station:
            say(radio_station.replace("1X ", ""))
            continue

        try:
            with open(RADIO_STATIONS, "r", encoding="utf-8") as f:
                station_list = json.load(f)

            stations = {entry["name"].lower(): entry["url"] for entry in station_list}

        except FileNotFoundError:
            say("Radiosender-Datei nicht gefunden.")
            return
        except json.JSONDecodeError:
            say("Fehler beim Laden der Radiosender-Datei.")
            return

        if radio_station not in stations:
            say(f"Ich konnte keinen Sender namens '{radio_station}' finden.")
            return

        url = stations[radio_station]
        say(f"Spiele {radio_station} ...")
        print(url)
        player = vlc.MediaPlayer(url)
        player.play()



def play_radio_TEST():
    while True:
        radio_station = "ffh"

        if "1X " in radio_station:
            say(radio_station.replace("1X ", ""))
            continue

        try:
            with open(RADIO_STATIONS, "r", encoding="utf-8") as f:
                station_list = json.load(f)

    
            stations = {entry["name"].lower(): entry["url"] for entry in station_list}

            radio_station = radio_station.lower()
            if radio_station not in stations:
                say(f"Ich konnte keinen Sender namens '{radio_station}' finden.")
                print("Nicht gefunden")
                return

            url = stations[radio_station]
            say(f"Spiele {radio_station} ...")
            print(url)
            player = vlc.MediaPlayer(url)
            player.play()
            break

        except FileNotFoundError:
            say("Radiosender-Datei nicht gefunden.")
            return
        except json.JSONDecodeError:
            say("Fehler beim Laden der Radiosender-Datei.")
            return

play_radio_TEST()