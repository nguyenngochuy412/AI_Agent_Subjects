from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models.message import Message
from app.schemas.chat import ChatRequest, ChatResponse, HistoryResponse, MessageOut

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def chat(payload: ChatRequest, db: AsyncSession = Depends(get_db)) -> ChatResponse:
    reply="Chao ban"
    db.add_all(
        [
            Message(user_id=payload.user_id, role="user", content=payload.message),
            Message(user_id=payload.user_id, role="assitant", content=reply),
        ]
    )
    await db.commit()
    return ChatResponse(reply=reply)

@router.get("/history/{user.id}", response_model=HistoryResponse)
async def history(
    user_id: str,
    limit: int = Query(50, ge=1, le=200),
    db: AsyncSession = Depends(get_db),
) -> HistoryResponse:
    stmt = (
        select(Message)
        .where(Message.user_id == user_id)
        .order_by(Message.id.desc())
        .limit(limit)
    )
    rows = (await db.scalars(stmt)).all()
    return HistoryResponse(
        user_id=user_id,
        messages=[MessageOut.model_validate(r) for r in reversed(rows)],
    )