from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field

class ChatRequest(BaseModel):
    user_id: str = Field(...,  min_length=1, max_length=64)
    message: str = Field(..., min_length=1, max_length=2000)


class ChatResponse(BaseModel):
    reply: str

class MessageOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    role: str
    content: str
    created_at: datetime

class HistoryResponse(BaseModel):
    user_id: str
    messages: list[MessageOut]