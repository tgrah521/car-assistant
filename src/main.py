import subprocess
import threading
from googleapiclient.discovery import build
import os
import socket
import time
from dotenv import load_dotenv
from listener import handle_voice_command
from voice import say


def is_connected():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=2)
        return True
    except OSError:
        return False

def wait_for_connection():
    while not is_connected():
        time.sleep(2)

def main():
    subprocess.Popen(["python", "obd_assistant.py"])
    if not is_connected():
        say("Netzwerkverbindung fehlgeschlagen")
        wait_for_connection()
    handle_voice_command()

if __name__ == "__main__":
    main()
