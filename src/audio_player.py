import subprocess
import threading
from googleapiclient.discovery import build
import os
from dotenv import load_dotenv
from listener import say
import time

load_dotenv()

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

def get_direct_audio_url(youtube_url):

    command = [
        "yt-dlp",
        "-f", "bestaudio",
        "-g",  
        youtube_url
    ]
    result = subprocess.run(command, capture_output=True, text=True, check=True)
    return result.stdout.strip()


def stream_and_download(song, output_path):
    say("Ich suche nach")
    say(song)
    video_url = get_video_url(song)

    try:
        direct_url = get_direct_audio_url(video_url)
        print(f"Direkte Audio-URL erhalten: {direct_url}")

        subprocess.Popen(["cvlc", "--play-and-exit", "--no-video", direct_url])
        print("VLC wurde gestartet, Audio-Streaming läuft!")

        #threading.Thread(target=download_mp3, args=(video_url, output_path)).start()

    except Exception as e:
        say(f"Fehler beim Starten des Streams")

def get_video_url(query):
    youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
    request = youtube.search().list(
        q=query,
        part='id',
        type='video',
        maxResults=1
    )
    response = request.execute()
    video_id = response['items'][0]['id']['videoId']
    return f'https://www.youtube.com/watch?v={video_id}'

def download_mp3(video_url, output_path):
    try:
        print(f"Downloading audio from: {video_url}")
        clean_title = "downloaded_audio"
        mp3_file_path = os.path.join(output_path, f"{clean_title}.mp3")

        command = [
            "yt-dlp",
            "--extract-audio",
            "--audio-format", "mp3",
            "--audio-quality", "192k",
            "-o", os.path.join(output_path, f"{clean_title}.%(ext)s"),
            video_url
        ]

        subprocess.run(command, check=True)

        current_mp3_file_path = os.path.join(output_path, "current.mp3")

        if os.path.exists(current_mp3_file_path):
            os.remove(current_mp3_file_path)

        os.rename(mp3_file_path, current_mp3_file_path)

        print(f"Downloaded and saved as: {current_mp3_file_path}")
        return current_mp3_file_path

    except Exception as e:
        print(f"Fehler beim MP3-Download: {e}")
        return None
    

def play_mp3(path,sleepTime):
    command = ["vlc", "--play-and-exit",path]
    subprocess.Popen(command)
    time.sleep(sleepTime)
    return

