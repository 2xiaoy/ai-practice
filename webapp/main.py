import os
from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
from openai import OpenAI

client = OpenAI(
    api_key=os.environ["DEEPSEEK_API_KEY"],
    base_url="https://api.deepseek.com"
)

app = FastAPI()

class ChatRequest(BaseModel):
    message: str

@app.get("/")
def home():
    return FileResponse(Path(__file__).parent / "index.html")

@app.post("/chat")
def chat(req: ChatRequest):
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "user", "content": req.message}]
    )
    return {"reply": response.choices[0].message.content}