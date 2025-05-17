import os
import random
from log import writelog
from voice import say, recognize_text
from audio_player import stream_and_download, get_video_duration
import time
from vlc_manager import close_all_vlc
import threading
import shutil

FILE_PATH = os.path.join(os.path.dirname(__file__), '../resource/playlist.txt')

def playlist_add():
    song = recognize_text("Welchen song wollen sie hinzufügen?")
    while True:
        confirmation = recognize_text(f"Ist {song} korrekt?")
        if "ja" in confirmation.lower():
            write_in_playlist(song)
            return
        elif "abbrechen" in confirmation.lower():
            return
        elif "nein" in confirmation.lower():
            playlist_add()
        else:
            continue
        
def playlist_remove():
    say("Ich entferne den letzten song aus der liste")
    remove_last_song()

def playlist_delete():
    say("Ich leere die Playlist")
    clear_playlist()

def playlist_start(KOPIEREN):
    threading.Thread(target=start_playlist, args=(KOPIEREN,)).start()

def playlist_load():
    load_playlist()

def playlist_save():
    playlist_name = recognize_text("Wie soll die Wiedergabeliste heißen?")
    while True:
        confirmation = recognize_text(f"Ist {playlist_name} korrekt?")
        if "ja" in confirmation.lower():
            save_playlist(playlist_name)
            return
        elif "abbrechen" in confirmation.lower() :
            return
        elif "nein" in confirmation.lower():
            playlist_save()
        else:
            continue
        


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



def start_playlist(kopieren):

    while True:
        songs = read_playlist()
        if not songs:
            say("Deine Liste scheint leer zu sein")
            break
        for x in songs:

            video_length = stream_and_download(x, ".", kopieren)
            print(f"Spiele Song: {x} für {video_length} Sekunden")
            time.sleep(video_length + 7)
            close_all_vlc()
    
def save_playlist(name):
    try:
        DESTINATION = os.path.join(os.path.dirname(__file__), f'../resource/playlists/{name}.txt')
        shutil.copy(FILE_PATH, DESTINATION)
        print(f'Playlist saved to {DESTINATION}')
        say(f"Wiedergabeliste wurde erfolgreich gespeichert")
    except Exception as e:
        print(f'Error saving playlist: {e}')
        say("Ein Fehler ist aufgetreten")
        writelog(f"playlist - save_playlist() {e}")

def load_playlist():
    try:
        playlist_name = recognize_text("Wie heißt die Wiedergabeliste?")
        if not playlist_name:
            say("Ich habe keinen Namen verstanden.")
            return

        filename = f"{playlist_name}.txt"
        playlist_dir = os.path.join(os.path.dirname(__file__), "../resource/playlists")
        available_playlists = os.listdir(playlist_dir)

        if filename in available_playlists:
            source_path = os.path.join(playlist_dir, filename)
            shutil.copy(source_path, FILE_PATH)
            say(f"Ich habe die Wiedergabeliste {playlist_name} geladen.")
        else:
            say(f"Ich konnte keine Wiedergabeliste mit dem Namen {playlist_name} finden.")
            return

    except Exception as e:
        writelog(f"playlist - load_playlist(): {e}")
        say("Beim Laden der Wiedergabeliste ist ein Fehler aufgetreten.")

