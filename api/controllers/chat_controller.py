from fastapi import APIRouter
from models.question import QuestionRequest
from services.chat_service import generate_conversation_response, generate_response

router = APIRouter()

@router.post("/chat")
async def chat(request: QuestionRequest):
    user_input = request.question
    response = generate_conversation_response(user_input)
    return {"response": response}
