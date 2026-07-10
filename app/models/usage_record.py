"""AI tool usage tracking model — extensible for membership tiers."""

from datetime import datetime

from sqlalchemy import DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class UsageRecord(Base):
    __tablename__ = "usage_records"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    visitor_id: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    tool_slug: Mapped[str] = mapped_column(String(255), nullable=False)
    user_tier: Mapped[str] = mapped_column(String(32), nullable=False, default="guest")
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), index=True)
