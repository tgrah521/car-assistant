# car-assistant
**Ein sprachgesteuerter Assistent für dein Auto**, der mit **OBD-II-Daten** arbeitet,
🎶 Musik streamt, 💬 WhatsApp-Nachrichten verschickt und sogar mit 🤖 KI deine Fragen beantwortet.  
Ideal für den **Raspberry Pi** in Kombination mit einem **ELM327 OBD-II Adapter**!

Features
* Voice Activation: Aktiviere den Assistenten per Sprachbefehl ("Hey", "Hallo", "BMW") oder über einen Button an GPIO PIN 17.

* KI-Fragen stellen: Stell beliebige Fragen – beantwortet von Google Gemini (gemini-pro).

* Musikstreaming: Streame Musik von YouTube durch einfache Sprachbefehle.

* WhatsApp Integration: Sende Nachrichten an deine Kontakte aus einer lokalen kontakte.json Datei.

* Zufälliger Song aus Datei: Spiele zufällige Songs aus recently_played.txt ab.

* Fahrzeug-Warnsystem: Benachrichtigt dich bei:

* Hoher Drehzahl bei niedriger Geschwindigkeit

* Niedriger Drehzahl bei Bewegung

* Hoher Kühlmitteltemperatur

* Niedriger Kühlmitteltemperatur bei hoher Drehzahl

* Tankstand-Ansage: Der Assistent liest bei Start den Tankfüllstand vor.

🔑 Anforderungen
* Raspberry Pi

* ELM327 OBD-II Adapter

* Mikrofon

* Lautsprecher

* .env Datei mit folgenden Inhalten:

   * AI_API_KEY=dein_gemini_api_key
   * YOUTUBE_API_KEY=dein_youtube_api_key

# Dependencies:

* KI und Google APIs
  * google-generativeai
  * google-api-python-client

* Sprachsteuerung und TTS
   * speechrecognition
   * pyttsx3
   * pyaudio               

* Fahrzeugdaten via OBD
  * obd

* System/Umgebungsvariablen
  * python-dotenv

