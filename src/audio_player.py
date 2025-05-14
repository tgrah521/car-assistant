import shutil
import subprocess
import threading
from googleapiclient.discovery import build
import os
from dotenv import load_dotenv
from voice import say
import time
from pathlib import Path
from load_songs import write_in_file, get_random_song
import isodate
from log import writelog
from vlc_manager import close_all_vlc


load_dotenv(dotenv_path=Path(__file__).resolve().parents[1] / '.env')
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
VIDEO_LENGTH = 0

def get_direct_audio_url(youtube_url):

    command = [
        "yt-dlp",
        "-f", "bestaudio",
        "-g",
        youtube_url
    ]
    result = subprocess.run(command, capture_output=True, text=True, check=True)
    return result.stdout.strip()


def stream_and_download(song, output_path, kopieren):
    say("Ich suche nach")
    say(song)
    video_url = get_video_url(song)

    try:
        direct_url = get_direct_audio_url(video_url)
        print(f"Direkte Audio-URL erhalten: {direct_url}")

        subprocess.Popen(["cvlc", "--play-and-exit", "--no-video", direct_url])
        print("VLC wurde gestartet, Audio-Streaming läuft!")
        try:
            write_in_file(song)
        except:
            say("Song konnte nicht in die liste geschrieben werden")
        if kopieren:
            threading.Thread(target=download_mp3, args=(video_url, output_path, song)).start()

    except Exception as e:
        say(f"Fehler beim Starten des Streams")
        writelog(f"audio_player - stream_and_download(): {e}")

def get_video_url(query):
    global VIDEO_LENGTH
    youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
    request = youtube.search().list(
        q=query,
        part='id',
        type='video',
        maxResults=1
    )
    response = request.execute()
    video_id = response['items'][0]['id']['videoId']
    VIDEO_LENGTH = get_video_duration(video_id)
    return f'https://www.youtube.com/watch?v={video_id}'

def get_video_length(query):
    youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
    request = youtube.search().list(
        q=query,
        part='id',
        type='video',
        maxResults=1
    )
    response = request.execute()
    video_id = response['items'][0]['id']['videoId']
    return get_video_duration(video_id)

def get_video_duration(video_id):
    youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
    request = youtube.videos().list(
        part='contentDetails',
        id=video_id
    )
    response = request.execute()
    duration = response['items'][0]['contentDetails']['duration']

    return get_duration_in_seconds(duration)


def get_duration_in_seconds(duration_str):
    duration = isodate.parse_duration(duration_str)
    return int(duration.total_seconds())



def download_mp3(video_url, output_path, song):
    try:
        output_path = "/home/tgrah/Musik"
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
        try:
            auto_copy(song)
            play_mp3(os.path.join(os.path.dirname(__file__), '../resource/success.mp3'),0)
        except:
            say("Fehler beim kopieren")
        return current_mp3_file_path

    except Exception as e:
        print(f"Fehler beim MP3-Download: {e}")
        return None


def play_mp3(path,sleepTime):
    command = ["vlc", "--play-and-exit",path]
    subprocess.Popen(command)
    time.sleep(sleepTime)
    return


def auto_copy(song):
    try:
        print("Now trying to copy mp3 to USB...")
        usb_mount_points = [os.path.join('/media/tgrah', d) for d in os.listdir('/media/tgrah') if os.path.isdir(os.path.join('/media/tgrah', d))]
        current_mp3_file_path = "/home/tgrah/Musik/current.mp3"

        if os.path.exists("/home/tgrah/Musik/fixed_current.mp3"):
            os.remove("/home/tgrah/Musik/fixed_current.mp3")

        if usb_mount_points:
            for mount_point in usb_mount_points:
                usb_file_path = os.path.join(mount_point, "current.mp3")
                while True:
                    fixed_mp3_file_path = fix_mp3(current_mp3_file_path, "/home/tgrah/Musik")
                    if fixed_mp3_file_path:
                        safe_song_name = "".join(c if c.isalnum() or c in " -_()" else "_" for c in song)
                        shutil.copy(fixed_mp3_file_path, os.path.join(mount_point, f"{safe_song_name}.mp3"))
                        os.remove(fixed_mp3_file_path)
                        return True
            return False
        return False
    except Exception as e:
        print(f"there was a Oupsie while Copy to your USB Flash drive with {song}: {e}")
        writelog(f"audio_player - auto_copy(): {e}")
        say("Ein unerwarteter Fehler ist aufgetreten")

def start_auto_play(KOPIEREN):
    threading.Thread(target=auto_play, args=(KOPIEREN,)).start()

def auto_play(kopieren):

    while True:
        song = get_random_song()
        if not song:
            say("Deine Liste scheint leer zu sein")
            break

        stream_and_download(song, ".", kopieren)
        print(f"Spiele Song: {song} für {VIDEO_LENGTH} Sekunden")
        time.sleep(VIDEO_LENGTH + 7)
        close_all_vlc()


def fix_mp3(mp3_file_path, output_path):
    try:
        # Sicherstellen, dass das Ausgangsverzeichnis existiert
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        
        # Pfad der gefixten MP3-Datei
        fixed_mp3_file_path = os.path.join(output_path, "fixed_current.mp3")
        
        # Vollständiger Pfad zu ffmpeg
        ffmpeg_path = "/usr/bin/ffmpeg"  # Vollständiger Pfad zu ffmpeg auf dem Raspberry Pi

        # ffmpeg-Befehl zum Konvertieren der MP3-Datei
        command = [
            ffmpeg_path, "-i", mp3_file_path, 
            "-b:a", "256k",  # Bitrate auf 256 kbps setzen
            fixed_mp3_file_path
        ]
        
        # Ausgabe des Kommandos zu Debugging-Zwecken
        print(f"Ausführen des Befehls: {' '.join(command)}")
        
        # ffmpeg-Befehl ausführen
        subprocess.run(command, check=True)
        
        return fixed_mp3_file_path
    except subprocess.CalledProcessError as e:
        print("ffmpeg error:", e.stderr)
        return None
    except Exception as e:
        print("Fehler beim Fixen der MP3:", e)
        return None