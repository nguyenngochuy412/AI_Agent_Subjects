from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_api_key
from app.db.session import get_db
from app.models.api_key import ApiKey

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


async def get_current_user_id(
    api_key: str | None = Depends(api_key_header),
    db: AsyncSession = Depends(get_db),
) -> str:
    if not api_key:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Missing API key")

    stmt = select(ApiKey).where(
        ApiKey.key_hash == hash_api_key(api_key),
        ApiKey.is_active.is_(True),
    )
    record = await db.scalar(stmt)
    if record is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid API key")
    return record.user_id