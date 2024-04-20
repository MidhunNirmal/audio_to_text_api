from typing import Union
import requests
from fastapi import FastAPI
import speech_recognition as sr
from io import BytesIO

app = FastAPI()

@app.post("/audio")
def read_root(audio_uri: str):
    try:
        # Download the audio file from the URI
        response = requests.get(audio_uri)
        response.raise_for_status()  # Raise an exception for non-200 status codes
        
        # Load audio data from the response content
        audio_data = BytesIO(response.content)
        
        # Perform speech recognition
        r = sr.Recognizer()
        with sr.AudioFile(audio_data) as source:
            audio = r.record(source)  # Extract audio data
            
        transcription = r.recognize_google(audio)  # Use Google Speech Recognition
        
        return {"transcription": transcription}
    
    except Exception as e:
        return {"error": str(e)}
