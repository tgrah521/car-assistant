import subprocess
import threading
from googleapiclient.discovery import build
import os
import socket
import time
from dotenv import load_dotenv
from listener import handle_voice_command
from audio_player import play_mp3
from voice import say
from network import check_for_connection

INTRO_MP3 = os.path.join(os.path.dirname(__file__), '../resource/intro.mp3')


def main():
    play_mp3(INTRO_MP3, 0)
    try:
        subprocess.Popen(["python", "obd_assistant.py"])
    except:
        print("Fehler bei der OBD verbindung")
    check_for_connection()
    say("Netzwerkverbindung erfolgreich")
    handle_voice_command()

if __name__ == "__main__":
    main()