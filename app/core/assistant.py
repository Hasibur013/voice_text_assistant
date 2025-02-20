# app/core/assistant.py
from app.core.groq_client import GroqClient
from app.core.speech import SpeechHandler

class Assistant:
    def __init__(self):
        self.groq_client = GroqClient()
        self.speech_handler = SpeechHandler()
    
    async def process_text_input(self, text: str):
        response_text = await self.groq_client.process_input(text)
        audio_filename = await self.speech_handler.text_to_speech(response_text)
        
        return {
            "text_response": response_text,
            "audio_response": audio_filename
        }
    
    async def process_voice_input(self, audio_file_path: str):
        text_input = await self.speech_handler.speech_to_text(audio_file_path)
        return await self.process_text_input(text_input)