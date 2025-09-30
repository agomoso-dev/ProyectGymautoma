import os
import requests
from fastapi import FastAPI, Response
from pydantic import BaseModel

app = FastAPI()

OLLAMA_SERVER_URL = os.getenv("OLLAMA_SERVER_URL", "http://ollama:11434")

# Petición GET para probar el server
@app.get('/')
def home():
    return {"Chat": "Bot"}

# GET
@app.get('/ask')
def ask(prompt: str):
    try:
        res = requests.post(f"{OLLAMA_SERVER_URL}/api/generate", json={
            "prompt": prompt,
            "stream": False,
            "model": "qwen2.5:0.5b" 
        })
        return Response(content=res.text, media_type="application/json")
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

# POST
class PromptRequest(BaseModel):
    prompt: str
    
@app.post('/ask')
def ask_post(data: PromptRequest):
    try:
        res = requests.post(f"{OLLAMA_SERVER_URL}/api/generate", json={
            "prompt": data.prompt,
            "stream": False,
            "model": "qwen2.5:0.5b" 
        })
        return Response(content=res.text, media_type="application/json")
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}
