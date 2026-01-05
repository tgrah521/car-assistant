import time
import obd
from audio_player import play_mp3
from voice import say
import os
import RPi.GPIO as GPIO

old_coolant_temp = None
FUEL_LEVEL_WARNING = 50
MIN_COOLANT_TEMP = 80
MAX_COOLANT_TEMP = 120
SERVO_PIN = 18
SERVO_FREQ = 50
GPIO.setmode(GPIO.BCM)
GPIO.setup(SERVO_PIN, GPIO.OUT)
servo = GPIO.PWM(SERVO_PIN, SERVO_FREQ)
servo.start(0)
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
    return True

def car_warning():
    global connection
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
                if rpm_query.value.magnitude > 3000 and speed_query.value.magnitude < 100:
                    play_mp3(WARNING_MP3, 0)
            except Exception as e:
                print(f"Fehler beim lesen der Drehzahl: {e}")

        if coolant_temp_query and coolant_temp_query.value is not None:
            try:
                temp = coolant_temp_query.value.magnitude
                update_servo(temp)
            except Exception as e:
                print(f"Fehler bei Verarbeitung der Kühlmitteltemperatur: {e}")
        if (coolant_temp_query and coolant_temp_query.value is not None) and \
           (rpm_query and rpm_query.value is not None):
            try:
                if coolant_temp_query.value.magnitude < 70 and rpm_query.value.magnitude > 2000:
                    play_mp3(WARNING_MP3, 0)
            except Exception as e:
                print(f"Fehler bei Überprüfung der Bedingungen. Kühlwasser{coolant_temp_query.value.magnitude} drehzahl:{rpm_query.value.magnitude}: {e}")

        time.sleep(1)


def update_servo(temp):
    global old_coolant_temp
    if temp is None:
        return

    if temp < MIN_COOLANT_TEMP or temp > MAX_COOLANT_TEMP or temp == old_coolant_temp or (temp < old_coolant_temp + 3 and temp > old_coolant_temp - 3):
        return

    angle(temp)
    old_coolant_temp = temp

def temp_to_angle(temp):
    temp = max(80, min(120, temp))
    angle = 4.5 * temp - 360
    angle = max(0, min(180, angle))
    angle = 180 - angle
    return angle

def angle(temp, hold_time=4):
    angle = temp_to_angle(temp)
    duty = 2 + angle / 18

    time.sleep(hold_time)
    servo.ChangeDutyCycle(duty)
    time.sleep(1)
    servo.ChangeDutyCycle(0)


def initial_connection_sound(is_connected):
    global connection
    global FUEL_LEVEL_WARNING
    try:
        if is_connected:
            play_mp3(SUCCESS_MP3, 2)
            fuel_level = connection.query(obd.commands.FUEL_LEVEL).value.magnitude
            say(f"Tanklevel: {round(fuel_level, 2)} prozent")
            angle(81)
            angle(118)
            angle(81)
            while fuel_level < FUEL_LEVEL_WARNING:
                FUEL_LEVEL_WARNING -= 10
        else:
            say("die OBD Verbindung ist fehlgeschlagen")
    except Exception as e:
        say("Fehler beim ansagen des Füllstandes")
        print(f"Fehler beim ansagen des Füllstandes: {e}")

angle(119,0)
angle(81,0)
initial_connection_sound(connect())
car_warning()
