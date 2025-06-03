import vlc
import time
from voice import say, recognize_text

def play_radio():
    while True:
        radio_station = recognize_text("Welchen Radiosender möchten Sie hören?")

        if "1X " in radio_station:
            say(radio_station.replace("1X ", ""))
            continue

        try:
            with open(RADIO_STATIONS, "r", encoding="utf-8") as f:
                station_list = json.load(f)

            stations = {entry["name"]: entry["url"] for entry in station_list}

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

        player = vlc.MediaPlayer(url)
        player.play()