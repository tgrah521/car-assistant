import socket
import time

def check_for_connection():
    if not is_connected():
        wait_for_connection()
    else:
        print("Netzverbindung besteht")

def is_connected():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=2)
        return True
    except OSError:
        return False

def wait_for_connection():
    while not is_connected():
        time.sleep(2)