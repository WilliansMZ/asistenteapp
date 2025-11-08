from fastapi import FastAPI
from pydantic import BaseModel
import requests, json

app = FastAPI()

class Query(BaseModel):
    message: str

@app.post("/ask")
async def ask_ai(query: Query):
    try:
        with requests.post(
    "http://localhost:11434/api/generate",
    json={"model": "gemma3:4b", "prompt": query.message},
    stream=True,
    timeout=60
) as response:
            if response.status_code != 200:
                return {"error": f"Error desde Ollama: {response.text}"}

            reply = ""
            for line in response.iter_lines():
                if line:
                    try:
                        data = json.loads(line.decode("utf-8"))
                        reply += data.get("response", "")
                    except json.JSONDecodeError:
                        continue

            return {"reply": reply.strip() or "No se recibió respuesta del modelo."}

    except Exception as e:
        return {"error": str(e)}

@app.get("/")
async def root():
    return {"message": "Servidor FastAPI + Ollama activo 🚀"}
