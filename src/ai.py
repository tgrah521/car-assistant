import google.generativeai as genai
from dotenv import load_dotenv
from voice import recognize_text, say
import os
from log import writelog

load_dotenv()

AI_API_KEY = os.getenv("AI_API_KEY")

def ask_question():
    try:
        question = get_question()
        if question is None:
            say("Ich breche den vorgang ab.")
            return
    
        genai.configure(api_key=AI_API_KEY)
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(question)
        say(response.text)
        return
    except Exception as e:
        say("Ein fehler ist aufgetreten")
        print("Ein fehler ist aufgetreten")
        writelog(f"ai - ask_question: {e}")

def get_question():
    while True:
        question = recognize_text("Stelle mir deine Frage")
        if "1X " in question:
            say("Entschuldigung. ich konnte deine Frage leider nicht verstehen")
            continue
        else:
            while True:
                confirmation = recognize_text("Ich habe verstanden: " + question + ". Ist das Korrekt?")
                if confirmation is None:
                    return None
                elif "ja" in confirmation.lower():
                    return question
                elif "nein" in confirmation.lower():
                    continue
                elif "abbrechen" in confirmation.lower():
                    return None
                else:
                    continue

