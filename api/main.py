from fastapi import FastAPI, Depends, HTTPException, status, Header
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from langchain_groq import ChatGroq
from langchain.schema import SystemMessage, HumanMessage
import os
from jose import jwt
import re
import json

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def verify_token(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Not authenticated")
    token = authorization.split(" ", 1)[1]
    secret = os.getenv("SUPABASE_JWT_SECRET")
    if not secret:
        raise HTTPException(status_code=500,
                            detail="SUPABASE_JWT_SECRET not configured")
    try:
        payload = jwt.decode(token, secret, algorithms=["HS256"])
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid token")
    return payload

class TaleRequest(BaseModel):
    description: str

@app.post("/generate-story")
async def generate_story(req: TaleRequest, payload=Depends(verify_token)):
    return {"tale": f"Once upon a time about {req.description}"}

class TaleAIRequest(BaseModel):
    prompt: str

@app.post("/generate-story-ai")
async def generate_story_ai(req: TaleAIRequest, payload=Depends(verify_token)):
    groq_api_key = os.getenv("GROQ_API_KEY")
    if not groq_api_key:
        return {"error": "GROQ_API_KEY not set"}

    # Crea el modelo de chat Groq
    chat = ChatGroq(groq_api_key=groq_api_key, model="llama-3.3-70b-versatile", temperature=0.7)

    system_prompt = (
        "Eres un experto escritor de cuentos infantiles. "
        "Escribe un cuento original dividido en capítulos, "
        "cada capítulo debe tener un título y un texto breve. "
        "Devuelve SOLO la respuesta en formato JSON con la estructura: "
        "{\"chapters\": [{\"title\": \"...\", \"text\": \"...\"}, ...]}"
    )

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=req.prompt)
    ]

    response = chat(messages)

    def extract_json(text):
        match = re.search(r'\{.*\}', text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group())
            except Exception:
                return None
        return None

    story_json = extract_json(response.content)
    if not story_json:
        return {"error": "No se pudo extraer el JSON", "raw": response.content}
    return story_json
