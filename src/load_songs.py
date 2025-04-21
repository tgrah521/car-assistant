import os
import random

def write_in_file(song):
    song = song + "\n"
    with open("recently_played.txt", "a") as f:
        f.write(song)

def read_file():
    try:
        if not os.path.exists("recently_played.txt"):
            open("recently_played.txt", "w").close()
            return

        with open("recently_played.txt", "r") as file:
            content = file.read().strip()

        if not content:
            return

        return content.split("\n")

    except Exception as e:
        return []
def get_random_song():
    try:
        arr = read_file()
        index = random.randint(0,len(arr))
        return arr[index-1]
    except Exception as e:
        return ""