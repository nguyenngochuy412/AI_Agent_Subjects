# from datetime import datetime

# from sqlalchemy import DateTime, String, Text, func
# from sqlalchemy.orm import Mapped, mapped_column

# from app.db.base import Base


# class Message(Base):
#     __tablename__ = "messages"

#     id: Mapped[int] = mapped_column(primary_key=True)
#     user_id: Mapped[str] = mapped_column(String(64), index=True)
#     role: Mapped[str] = mapped_column(String(16))  # "user" hoặc "bot"
#     content: Mapped[str] = mapped_column(Text)
#     created_at: Mapped[datetime] = mapped_column(
#         DateTime(timezone=True), server_default=func.now()
#     )