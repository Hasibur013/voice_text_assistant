# app/api/routes.py
import subprocess
import tempfile
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import aiofiles
import os

from groq import BaseModel
from app.core.assistant import Assistant
from app.config import get_settings

router = APIRouter()
assistant = Assistant()
settings = get_settings()

class TextInput(BaseModel):
    text: str

@router.post("/text")
async def process_text(input_data: TextInput):
    """
    input_data will have a `text` attribute from the JSON body.
    Example of valid JSON:
    {
        "text": "Hello world"
    }
    """
    try:
        response = await assistant.process_text_input(input_data.text)
        return JSONResponse(content=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# @router.post("/text")
# async def process_text(text: str):
#     try:
#         response = await assistant.process_text_input(text)
#         return JSONResponse(content=response)
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))






# if use ffmpeg
@router.post("/voice")
async def process_voice(audio: UploadFile = File(...)):
    try:
        # 1) Save the uploaded file (likely .webm) to a temporary location
        with tempfile.NamedTemporaryFile(suffix=".webm", delete=False) as temp_file:
            file_data = await audio.read()
            temp_file.write(file_data)
            webm_path = temp_file.name

        try:
            # 2) Convert WebM -> WAV using ffmpeg
            wav_path = webm_path.replace(".webm", ".wav")
            command = [
                "ffmpeg",
                "-i", webm_path,
                "-ar", "16000",  # sample rate
                "-ac", "1",      # mono
                wav_path
            ]
            subprocess.run(command, check=True)

            # 3) Pass wav_path to your speech recognition / assistant code
            response = await assistant.process_voice_input(wav_path)
            return response  # or JSONResponse(content=response)

        finally:
            os.remove(webm_path)
            if os.path.exists(wav_path):
                os.remove(wav_path)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))












# When file upload
# @router.post("/voice")
# async def process_voice(audio: UploadFile = File(...)):
#     try:
#         # Create a temporary file to store the uploaded audio
#         suffix = os.path.splitext(audio.filename)[1].lower()
#         with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as temp_file:
#             # Save uploaded audio file
#             content = await audio.read()
#             temp_file.write(content)
#             temp_file_path = temp_file.name

#         try:
#             # Process the audio
#             response = await assistant.process_voice_input(temp_file_path)
#             return JSONResponse(content=response)
#         finally:
#             # Clean up the temporary file
#             os.remove(temp_file_path)
            
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
