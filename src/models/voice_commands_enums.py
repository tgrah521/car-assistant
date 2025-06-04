from enum import Enum, auto

class VoiceCommand(Enum):
    WHATSAPP = auto()
    MUSIK = auto()
    LOOP = auto()
    SPIELE = auto()
    FRAGE = auto()
    TANK = auto()
    KUEHLWASSER = auto()
    BATTERIE = auto()
    KOPIEREN = auto()
    PLAYLIST_ADD = auto()
    PLAYLIST_REMOVE = auto()
    PLAYLIST_CLEAR = auto()
    PLAYLIST_PLAY = auto()
    PLAYLIST_SAVE = auto()
    PLAYLIST_LOAD = auto()
    PLAYLIST_DELETE = auto()
    PLAYLIST_LIST = auto()
    HELP = auto()
    EXIT = auto()
    NAVIGATION = auto()
    RADIO = auto()

    @staticmethod
    def from_text(text: str):
        text = text.lower()
        if "whatsapp" in text:
            return VoiceCommand.WHATSAPP
        elif "musik" in text:
            return VoiceCommand.MUSIK
        elif "spiele" in text:
            return VoiceCommand.SPIELE
        elif "frage" in text:
            return VoiceCommand.FRAGE
        elif "tank" in text:
            return VoiceCommand.TANK
        elif "kühlwasser" in text:
            return VoiceCommand.KUEHLWASSER
        elif "batterie" in text:
            return VoiceCommand.BATTERIE
        elif "kopieren" in text:
            return VoiceCommand.KOPIEREN
        elif "hilfe" in text:
            return VoiceCommand.HELP
        elif "zufall" in text:
            return VoiceCommand.LOOP
        elif "wiedergabeliste hinzufügen" in text:
            return VoiceCommand.PLAYLIST_ADD
        elif "wiedergabeliste leeren" in text:
            return VoiceCommand.PLAYLIST_CLEAR
        elif "wiedergabeliste entfernen" in text:
            return VoiceCommand.PLAYLIST_REMOVE
        elif "wiedergabeliste starten" in text:
            return VoiceCommand.PLAYLIST_PLAY
        elif "wiedergabeliste speichern" in text:
            return VoiceCommand.PLAYLIST_SAVE
        elif "wiedergabeliste laden" in text:
            return VoiceCommand.PLAYLIST_LOAD
        elif "wiedergabeliste löschen" in text:
            return VoiceCommand.PLAYLIST_DELETE
        elif "wiedergabelisten" in text:
            return VoiceCommand.PLAYLIST_LIST
        elif "beenden" in text:
            return VoiceCommand.EXIT
        elif "navigation" in text:
            return VoiceCommand.NAVIGATION
        elif "radio" in text:
            return VoiceCommand.RADIO

        return None
