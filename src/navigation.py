from voice import recognize_text, say

def set_route():
    while True:
        city = recognize_text("Nennen sie mir die Stadt")
        if "1X " in city:
            say(city.replace("1X ", ""))
            continue
        confirmation_city = recognize_text(f"Ist {city} korrekt ?")
        if "1X " in confirmation_city:
            say(confirmation_city.replace("1X ", ""))
            continue
        else:
            if "ja" in confirmation_city:
                say("Ok")
                break
            else:
                continue

    while True:
        street = recognize_text("Nennen sie mir die Strasse")
        if "1X " in street:
            say(street.replace("1X ", ""))
            continue
        confirmation_street = recognize_text(f"Ist {street} korrekt ?")
        if "1X " in confirmation_street:
            say(confirmation_street.replace("1X ", ""))
            continue
        else:
            if "ja" in confirmation_city:
                say("Ok")
                break
            else:
                continue

    while True:
        number = recognize_text("Nennen sie mir die Hausnummer")
        if "1X " in number:
            say(number.replace("1X ", ""))
            continue
        confirmation_number = recognize_text(f"Ist {number} korrekt ?")
        if "1X " in confirmation_number:
            say(confirmation_number.replace("1X ", ""))
            continue
        else:
            if "ja" in confirmation_city:
                say("Ok")
                break
            else:
                continue
   # start_navigation()

