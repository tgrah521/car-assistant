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
    HELP = auto()

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
        elif "zufalls" in text or "wiedergabe" in text:
            return VoiceCommand.LOOP
        return None
