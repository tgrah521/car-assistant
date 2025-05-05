import unittest
from unittest.mock import patch, MagicMock
from src.ai import ask_question  
from src.voice import recognize_text

class TestAskQuestion(unittest.TestCase):
    
    @patch("src.ai.say")
    @patch("src.ai.recognize_text")
    def test_empty_input(self, mock_recognize, mock_say):
        mock_recognize.return_value = ""
        ask_question()
        mock_say.assert_called_with("Entschuldigung. ich konnte deine Frage leider nicht verstehen")

    @patch("src.ai.genai")
    @patch("src.ai.say")
    @patch("src.ai.recognize_text")
    def test_valid_input(self, mock_recognize, mock_say, mock_genai):
        mock_recognize.return_value = "Was ist die Hauptstadt von Deutschland?"
        
        mock_model = MagicMock()
        mock_model.generate_content.return_value.text = "Berlin"
        mock_genai.GenerativeModel.return_value = mock_model

        ask_question()

        mock_say.assert_called_with("Berlin")
        mock_model.generate_content.assert_called_with("Was ist die Hauptstadt von Deutschland?")

if __name__ == "__main__":
    unittest.main()
