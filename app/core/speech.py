# app/core/speech.py
import speech_recognition as sr
from gtts import gTTS
import os
import uuid
from app.config import get_settings

class SpeechHandler:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.settings = get_settings()
    
    async def speech_to_text(self, audio_file_path: str) -> str:
        try:
            with sr.AudioFile(audio_file_path) as source:
                audio_data = self.recognizer.record(source)
                text = self.recognizer.recognize_google(audio_data)
                return text
        except Exception as e:
            return f"Error converting speech to text: {str(e)}"
    
    async def text_to_speech(self, text: str) -> str:
        try:
            filename = f"{uuid.uuid4()}.mp3"
            filepath = os.path.join(self.settings.audio_upload_dir, filename)
            
            tts = gTTS(text=text, lang='en')
            tts.save(filepath)
            
            return filename
        except Exception as e:
            return f"Error converting text to speech: {str(e)}"