import os
import random
from log import writelog

FILE_PATH = os.path.join(os.path.dirname(__file__), '../resource/recently_played.txt')

def write_in_file(song):
    song = song + "\n"
    with open(FILE_PATH, "a") as f:
        f.write(song)

def read_file():
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
def get_random_song():
    try:
        arr = read_file()
        index = random.randint(0,len(arr))
        return arr[index-1]
    except Exception as e:
        writelog(f"load_songs - get_random_song {e}")
        return ""   