from voice import say, recognize_text

def tell_all_voice_commands():
    message = "Ich höre derzeit auf folgende Voice commands:" \
    "Whatsapp, Musik, Spiele, Zufallswiedergabe, Frage, Tank, Kuehlwasser,  Batterie, Kopieren, Hilfe", 
    "Wiedergabeliste hinzufügen", "Wiedergabeliste entfernen", "Wiedergabeliste löschen" ,
    "wiedergabeliste starten, wiedergabeliste speichern"
    say(message)
    while True:
        confirmation = recognize_text("Soll ich diese genauer erklären?") 
        if confirmation.lower() == "ja":
            tell_details()
            return
        elif confirmation.lower() == "nein":
            say("ok")
            return 
        else:
            continue
        
def tell_details():
    say("Whatsapp! Schreibe eine Nachricht an einen bestimmten kontakt")
    say("Musik! Spielt ein zufälliges lied aus recently_played.txt")
    say("Spiele! sage danach den künstler und das gewünschte lied")
    say("Zufallswiedergabe!: Ich spiele bis ich unterbrochen werde zufaellige lieder aus recently_played.txt")
    say("Frage! Stelle eine frage an gemini")
    say("Tank! Gibt die Tankfüllung in prozent")
    say("kühlwasser! Gibt die temperatur in grad")
    say("Batterie! Gibt die spannung der batterie in volt")
    say("kopieren! Wenn kopieren aktiviert wurde, wird das angefragte lied auf den eingesteckten USB Stick kopiert")
    return
