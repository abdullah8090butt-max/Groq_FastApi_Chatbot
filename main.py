from fastapi import FastAPI
from pydantic import BaseModel
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

app = FastAPI()


class ChatRequest(BaseModel):
    question: str


@app.get("/")
def home():
    return {
        "message": "AI Chatbot API is running!"
    }


@app.post("/predict")
def predict(request: ChatRequest):

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "user",
                "content": request.question
            }
        ]
    )

    answer = response.choices[0].message.content

    return {
        "question": request.question,
        "answer": answer
    }