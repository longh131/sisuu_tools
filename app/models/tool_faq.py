"""Tool FAQ ORM model — maps to tool_faqs table."""

from sqlalchemy import ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class ToolFaq(Base):
    """FAQ entry associated with a specific tool."""

    __tablename__ = "tool_faqs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    tool_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("tools.id"), nullable=False, index=True
    )
    question: Mapped[str] = mapped_column(Text, nullable=False)
    answer: Mapped[str] = mapped_column(Text, nullable=False)
    sort_order: Mapped[int] = mapped_column(Integer, default=0)

    tool: Mapped["Tool"] = relationship("Tool", back_populates="faqs")
