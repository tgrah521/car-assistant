import os
import random
from log import writelog
from voice import say, recognize_text


FILE_PATH = os.path.join(os.path.dirname(__file__), '../resource/playlist.txt')

def playlist_add():
    song = recognize_text("Welchen song wollen sie hinzufügen?")
    while True:
        confirmation = recognize_text(f"Ist {song} korrekt?")
        if confirmation.lower() == "ja":
            write_in_playlist(song)
            return
        elif confirmation.lower() == "nein":
            return
        
def playlist_remove():
    say("Ich entferne den letzten song aus der liste")
    remove_last_song()

def playlist_delete():
    say("Ich leere die Playlist")
    clear_playlist()

        


def write_in_playlist(song):
    try:
        song = song + "\n"
        with open(FILE_PATH, "a") as f:
            f.write(song)
        say("Ich habe den Song aufgenommen")
    except Exception as e:
        writelog(f"playlist - write_in_playlist(): {e}")

def read_playlist():
    try:
        if not os.path.exists(FILE_PATH):
            open(FILE_PATH, "w").close()
            return

        with open(FILE_PATH, "r") as file:
            content = file.read().strip()

        if not content:
            return

        return content.split("\n")

    except Exception as e:
        writelog(f"load_songs - read_file(): {e}")
        return []
    
    
def clear_playlist():
    try:
        open(FILE_PATH, "w").close()
        print("Playlist wurde geleert.")
        say("Playlist wurde geleert.")
    except Exception as e:
        writelog(f"load_songs - clear_playlist(): {e}")
        say("Fehler beim lleren der Playlist")

def remove_last_song():
    try:
        if not os.path.exists(FILE_PATH):
            say("Die Playlist ist leer.")
            return

        with open(FILE_PATH, "r") as file:
            lines = file.readlines()

        if not lines:
            say("Die Playlist ist leer.")
            return

        lines = lines[:-1]

        with open(FILE_PATH, "w") as file:
            file.writelines(lines)

        say("Der letzte Song wurde entfernt.")
    except Exception as e:
        writelog(f"load_songs - remove_last_song(): {e}")
        say("Fehler beim Entfernen des letzten Songs.")
