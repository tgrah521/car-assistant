import vlc
import time
import json
import os
import threading
from voice import say, recognize_text
from log import writelog

RADIO_STATIONS = os.path.join(os.path.dirname(__file__), '../resource/radio_stations.json')
stop_event = threading.Event()
radio_thread = None

def start_radio_thread():
    global radio_thread
    try:
        stop_event.clear()
        radio_thread = threading.Thread(target=play_radio)
        radio_thread.start()
    except Exception as e:
        say("Beim starten des Radios ist ein fehler aufgetreten")
        print("Fehler beim starten des Senders")
        writelog(f"radio - start_radio_thread(): Fehler:{e}")

def stop_radio_thread():
    try:
        stop_event.set()
        if radio_thread is not None:
            radio_thread.join()
            print("Radio thread terminated.")
    except Exception as e:
        say("Beim stoppen des Radios ist ein fehler aufgetreten")
        print("Fehler beim stoppen des Senders")
        writelog(f"radio - sttop_radio_thread(): Fehler:{e}")


def play_radio():
    while not stop_event.is_set():
        radio_station = recognize_text("Welchen Radiosender möchten Sie hören?").lower()
        print(f"Radiosender:{radio_station}")
        if "1X " in radio_station:
            say(radio_station.replace("1X ", ""))
            continue

        try:
            with open(RADIO_STATIONS, "r", encoding="utf-8") as f:
                station_list = json.load(f)

            stations = {entry["name"].lower(): entry["url"] for entry in station_list}
            print("Liste gefunden")
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
        print(url)
        say(f"Spiele {radio_station} ...")
        print(f"Spiele {radio_station} ...")
        player = vlc.MediaPlayer(url)
        player.play()
        while not stop_event.is_set():
            state = player.get_state()
            print("State:", state)
            if state == vlc.State.Ended or state == vlc.State.Error:
                break
            time.sleep(1)