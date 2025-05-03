import subprocess
import threading
from googleapiclient.discovery import build
import os
from dotenv import load_dotenv
from voice import say
import time
from pathlib import Path

load_dotenv(dotenv_path=Path(__file__).resolve().parents[1] / '.env')
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


def stream_and_download(song, output_path, kopieren):
    say("Ich suche nach")
    say(song)
    video_url = get_video_url(song)

    try:
        direct_url = get_direct_audio_url(video_url)
        print(f"Direkte Audio-URL erhalten: {direct_url}")

        process = subprocess.Popen(["cvlc", "--play-and-exit", "--no-video", direct_url])
        print("VLC wurde gestartet, Audio-Streaming läuft!")
    
        if kopieren:
            threading.Thread(target=download_mp3, args=(video_url, output_path, song)).start()
        return process

    except Exception as e:
        say(f"Fehler beim Starten des Streams")

def get_video_url(query):
    print(YOUTUBE_API_KEY)
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
    usb_mount_points = [os.path.join('/media/tgrah', d) for d in os.listdir('/media/tgrah') if os.path.isdir(os.path.join('/media/tgrah', d))]
    current_mp3_file_path = "/home/tgrah/Musik/current.mp3"

    if os.path.exists("/home/tgrah/Musik/fixed_current.mp3"):
        os.remove("/home/tgrah/Musik/fixed_current.mp3")

    if usb_mount_points:
        for mount_point in usb_mount_points:
            usb_file_path = os.path.join(mount_point, "current.mp3")
            while True:
                # Benutzer nach einem Titel fragen
                title = song
                if title == "Kein Titel wurde abgespielt":
                    return False
                if title:
                    confirmation = "ja"
                    if "ja" in confirmation.lower() or "richtig" in confirmation.lower():
                        # Fixe die MP3-Datei, bevor sie auf den USB-Stick kopiert wird
                        fixed_mp3_file_path = fix_mp3(current_mp3_file_path, "/home/tgrah/Musik")
                        if fixed_mp3_file_path:
                            # Kopiere die gefixte Datei mit dem Titel als Dateinamen auf den USB-Stick
                            if FOLDER_NAME != "undefined":
                                shutil.copy(fixed_mp3_file_path, os.path.join(mount_point,FOLDER_NAME, f"{title}.mp3"))
                            else: 
                                shutil.copy(fixed_mp3_file_path, os.path.join(mount_point, f"{title}.mp3"))
                            os.remove(fixed_mp3_file_path)
                            return True
        return False
    return False


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