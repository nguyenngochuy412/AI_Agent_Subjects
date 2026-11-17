from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user_id
from app.db.session import get_db
from app.models.message import Message
from app.schemas.chat import ChatRequest, ChatResponse, HistoryResponse, MessageOut

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def chat(
    payload: ChatRequest,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
) -> ChatResponse:
    reply = "Chào bạn"
    db.add_all(
        [
            Message(user_id=user_id, role="user", content=payload.message),
            Message(user_id=user_id, role="assistant", content=reply),
        ]
    )
    await db.commit()
    return ChatResponse(reply=reply)


@router.get("/history", response_model=HistoryResponse)
async def history(
    limit: int = Query(50, ge=1, le=200),
    user_id: str = Depends(get_current_user_id),
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