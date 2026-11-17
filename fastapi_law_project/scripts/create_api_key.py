import asyncio
import sys

from app import models  # noqa: F401
from app.core.security import generate_api_key, hash_api_key
from app.db.session import Base, SessionLocal, engine
from app.models.api_key import ApiKey


async def main(user_id: str) -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    key = generate_api_key()
    async with SessionLocal() as db:
        db.add(ApiKey(key_hash=hash_api_key(key), user_id=user_id))
        await db.commit()
    await engine.dispose()

    print(f"user_id: {user_id}")
    print(f"API key (chỉ hiện một lần, hãy lưu lại): {key}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Cách dùng: python -m scripts.create_api_key <user_id>")
    asyncio.run(main(sys.argv[1]))