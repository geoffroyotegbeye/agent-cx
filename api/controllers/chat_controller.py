from fastapi import APIRouter
from models.question import QuestionRequest
from services.chat_service import generate_conversation_response
import logging

router = APIRouter()

logging.basicConfig(level=logging.INFO)

@router.post("/chat")
async def chat(request: QuestionRequest):
    logging.info(f"Question reçue : {request.question}")
    response = generate_conversation_response(request.question)
    logging.info(f"Réponse envoyée : {response}")
    print(f"Réponse complète : {response}")  # Vérifie ce qui est renvoyé dans la réponse
    return {"response": response}

