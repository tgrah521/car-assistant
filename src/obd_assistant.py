import time
import obd
from audio_player import play_mp3
from voice import say

CAR_WARNING = False
HIGH_SPEED = 110
connection = None

def connect():
    global CAR_WARNING
    global connection
    try:
        connection = obd.OBD()
        if connection.is_connected():
            CAR_WARNING = True
        else:
            print("Keine ODB Verbindung")
    except Exception as e:
        play_mp3("/home/tgrah/Dokumente/warning.mp3", 2)

def car_warning():
    try:
        global connection
        global HIGH_SPEED

        try:
            coolant_temp_query = connection.query(obd.commands.COOLANT_TEMP)
            rpm_query = connection.query(obd.commands.RPM)
            speed_query = connection.query(obd.commands.SPEED)
        except Exception as e:
            say("Fehler bei der Fahrzeugdiagnose.")
            return
        if speed_query and speed_query.value is not None:
            if speed_query.value.magnitude > HIGH_SPEED:
                say(HIGH_SPEED)
                HIGH_SPEED += 10 
        
            elif speed_query.value.magnitude < 90:  
                HIGH_SPEED = 110
        if speed_query and speed_query.value and rpm_query and rpm_query.value is not None:
            try:
                if rpm_query.value.magnitude < 600 and speed_query.value.magnitude > 10:
                    play_mp3("/home/tgrah/Dokumente/warning.mp3", 0)
            except Exception as e:
                print(f"Fehler: {e}")
        
        if rpm_query and rpm_query.value is not None:
            try:
                if rpm_query.value.magnitude > 3000 and speed_query.value.magnitude < 120:
                    play_mp3("/home/tgrah/Dokumente/warning.mp3", 0)
            except Exception as e:
                print(f"Fehler beim lesen der Drehzahl: {e}")
        
        if coolant_temp_query and coolant_temp_query.value is not None:
            try:
                if coolant_temp_query.value.magnitude > 110:
                    play_mp3("/home/tgrah/Dokumente/warning.mp3", 0)
            except Exception as e:
                print(f"Fehler bei Verarbeitung der Kühlmitteltemperatur: {e}")
        if (coolant_temp_query and coolant_temp_query.value is not None) and \
           (rpm_query and rpm_query.value is not None):
            try:
                if coolant_temp_query.value.magnitude < 80 and rpm_query.value.magnitude > 1800:
                    play_mp3("/home/tgrah/Dokumente/warning.mp3", 0)
            except Exception as e:
                print(f"Fehler bei Überprüfung der Bedingungen. Kühlwasser{coolant_temp_query.value.magnitude} drehzahl:{rpm_query.value.magnitude}: {e}")
        
        time.sleep(1)

    except Exception as e:
        print(f"Unbekannter Fehler in car_warning(): {e}")
        say("Ein schwerwiegender Fehler ist aufgetreten.")

connection = obd.OBD()
if connection.is_connected():
    CAR_WARNING = True
    play_mp3("/home/tgrah/Dokumente/success.mp3", 2)
    fuel_level = connection.query(obd.commands.FUEL_LEVEL).value.magnitude
    say(f"Tanklevel: {round(fuel_level, 2)} prozent") 
else:
    say("die OBD Verbindung ist fehlgeschlagen")
           
while True:
    time.sleep(2)
    if CAR_WARNING:
        car_warning()
    else:
        connect()
