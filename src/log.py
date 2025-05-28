from datetime import datetime
import os

def writelog(Message):

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    LOG_FILE_PATH= os.path.join(os.path.dirname(__file__), '../resource/logfile_car_system.log')

    try:
        with open(LOG_FILE_PATH, "a") as log_file:
            log_file.write(f"{current_time} - {Message}\n")

    except Exception as e:
        print(f"Fehler beim Schreiben in die Log-Datei: {e}")