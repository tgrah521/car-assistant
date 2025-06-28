import time
import obd
from audio_player import play_mp3
from voice import say
import os

HIGH_SPEED = 150
FUEL_LEVEL_WARNING = 50
connection = None
WARNING_MP3 = os.path.join(os.path.dirname(__file__), '../resource/warning.mp3')
SUCCESS_MP3 = os.path.join(os.path.dirname(__file__), '../resource/success.mp3')

def connect() -> bool:
    global connection
    while True:
        try:
            connection = obd.OBD()
            if connection.is_connected():
                break
            else:
                print("Keine ODB Verbindung")
        except Exception as e:
            print("Fehler beim versuch zu verbinden")
        time.sleep(2)
    return True

def car_warning():
    global connection
    global HIGH_SPEED
    global FUEL_LEVEL_WARNING
    while True:
        connect()
        try:
            coolant_temp_query = connection.query(obd.commands.COOLANT_TEMP)
            rpm_query = connection.query(obd.commands.RPM)
            speed_query = connection.query(obd.commands.SPEED)
            fuel_level = connection.query(obd.commands.FUEL_LEVEL)
        except Exception as e:
            say("Fehler bei der Fahrzeugdiagnose.")
            return
        
        if speed_query and speed_query.value is not None:
            if speed_query.value.magnitude > HIGH_SPEED:
                say(HIGH_SPEED)
                HIGH_SPEED += 10

            elif speed_query.value.magnitude < 90:
                HIGH_SPEED = 110

        if fuel_level and fuel_level.value is not None and fuel_level.value.magnitude < FUEL_LEVEL_WARNING:
            play_mp3(WARNING_MP3, 2)
            say(f"Tankelevel beträgt {FUEL_LEVEL_WARNING} prozent")
            FUEL_LEVEL_WARNING -= 10

        if speed_query and speed_query.value and rpm_query and rpm_query.value is not None:
            try:
                if rpm_query.value.magnitude < 700 and speed_query.value.magnitude > 10:
                    play_mp3(WARNING_MP3, 0)
            except Exception as e:
                print(f"Fehler: {e}")

        if rpm_query and rpm_query.value is not None:
            try:
                if rpm_query.value.magnitude > 3000 and speed_query.value.magnitude < 120:
                    play_mp3(WARNING_MP3, 0)
            except Exception as e:
                print(f"Fehler beim lesen der Drehzahl: {e}")

        if coolant_temp_query and coolant_temp_query.value is not None:
            try:
                if coolant_temp_query.value.magnitude > 110:
                    play_mp3(WARNING_MP3, 0)
            except Exception as e:
                print(f"Fehler bei Verarbeitung der Kühlmitteltemperatur: {e}")
        if (coolant_temp_query and coolant_temp_query.value is not None) and \
           (rpm_query and rpm_query.value is not None):
            try:
                if coolant_temp_query.value.magnitude < 80 and rpm_query.value.magnitude > 1800:
                    play_mp3(WARNING_MP3, 0)
            except Exception as e:
                print(f"Fehler bei Überprüfung der Bedingungen. Kühlwasser{coolant_temp_query.value.magnitude} drehzahl:{rpm_query.value.magnitude}: {e}")

        time.sleep(1)


def initial_connection_sound(is_connected):
    global connection
    global FUEL_LEVEL_WARNING
    try:
        if is_connected:
            play_mp3(SUCCESS_MP3, 2)
            fuel_level = connection.query(obd.commands.FUEL_LEVEL).value.magnitude
            say(f"Tanklevel: {round(fuel_level, 2)} prozent")
            while fuel_level + 10 < FUEL_LEVEL_WARNING:
                FUEL_LEVEL_WARNING -= 10
        else:
            say("die OBD Verbindung ist fehlgeschlagen")
    except Exception as e:
        say("Fehler beim ansagen des Füllstandes")
        print(f"Fehler beim ansagen des Füllstandes: {e}")

initial_connection_sound(connect())
car_warning()
