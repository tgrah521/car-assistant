import socket
import time
import pyttsx3

def check_for_connection():
    if not is_connected():
        say("Derzeit besteht keine Internetverbindung. Ich versuche mich zu verbinden")
        wait_for_connection()
    else: 
        return

def is_connected():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=2)
        return True
    except OSError:
        return False

def wait_for_connection():
    while not is_connected():
        time.sleep(2)

def get_ip_adress():
    try:
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)

        print("Your Computer IP Address is:" + IPAddr)
        say(IPAddr)
    except Exception as e:
        say("Fehler beim lesen der Ip-Adresse")
        print(f"Fehler beim lesen der Ip-Adresse{e}")

engine = pyttsx3.init()

def say(text):
    engine.getProperty('voices')

    engine.setProperty('pitch', 40)
    engine.setProperty('rate', 130)
    engine.setProperty('voice','german')
    engine.setProperty('text','normalize')
    engine.say(text)
    engine.runAndWait()