# app/core/groq_client.py
import groq
from app.config import get_settings

class GroqClient:
    def __init__(self):
        settings = get_settings()
        self.client = groq.Groq(api_key=settings.groq_api_key)
    
    async def process_input(self, input_text: str) -> str:
        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant that provides clear and concise responses."
                    },
                    {
                        "role": "user",
                        "content": input_text
                    }
                ],
                model="mixtral-8x7b-32768",
                temperature=0.7,
                max_tokens=1024
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            return f"Error processing request: {str(e)}"