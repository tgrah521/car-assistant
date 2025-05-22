import obd
from voice import say
from log import writelog


def say_obd_command(command):
    try:
        connection = obd.OBD()
        if connection.is_connected():
            if command == "FUEL_LEVEL":
                fuel_level = connection.query(obd.commands.FUEL_LEVEL).value.magnitude
                say(f"Tanklevel: {round(fuel_level, 2)} prozent")
            elif command == "COOLANT_TEMP":
                coolant_temp = connection.query(obd.commands.COOLANT_TEMP).value.magnitude
                say(f"Temperatur: {round(coolant_temp, 2)} Grad")
            elif command == "CONTROL_MODULE_VOLTAGE":
                voltage = connection.query(obd.commands.CONTROL_MODULE_VOLTAGE).value.magnitude
                say(f"Spannung: {round(voltage, 2)} Volt")
        else:
            say("Es besteht keine OBD verbindung")
    except Exception as e:
        print(f"Fehler {e}")
        writelog(f"obd_commands - say_obd_command(): {e}")
        say(f"Fehler: {e}")
