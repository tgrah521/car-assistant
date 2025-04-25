import google.generativeai as genai
from dotenv import load_dotenv
from voice import recognize_text, say
import os

load_dotenv()

AI_API_KEY = os.getenv("AI_API_KEY")

def ask_question():
    question = recognize_text("Stelle mir deine Frage")
    if question == "":
        say("Entschuldigung. ich konnte deine Frage leider nicht verstehen")
        return
    
    genai.configure(api_key=AI_API_KEY)
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(question)
    say(response.text)
    return

