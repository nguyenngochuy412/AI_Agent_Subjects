from fastapi import APIRouter

from app.schemas.chat import ChatRequest, ChatResponse

router = APIRouter(tags=["chat"])                                       


@router.post("/chat", response_model=ChatResponse)
def chat(payload: ChatRequest) -> ChatResponse:
    if payload.message == "hello":
        return ChatResponse(reply="Chào bạn")
    else:
        return ChatResponse(reply=f"Bạn vừa nói: {payload.message}")                                