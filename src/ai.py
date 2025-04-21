import google.generativeai as genai
from dotenv import load_dotenv
from listener import recognize_text, say
import os

load_dotenv()

AI_API_KEY = os.getenv("AI_API_KEY")

def ask_question():
    say("Stelle mir deine Frage")
    question = recognize_text()
    if question == "":
        say("Entschuldigung. ich konnte deine Frage leider nicht verstehen")
        return
    
    genai.configure(api_key=AI_API_KEY)
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(question)
    say(response.text)
    return

