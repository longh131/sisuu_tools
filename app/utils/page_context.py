"""Page context helper — merges base context with auth state."""

from fastapi import Request
from sqlalchemy.orm import Session

from app.services.auth_service import get_current_user
from app.utils.templates import base_context


def page_context(request: Request, db: Session | None = None, **extra) -> dict:
    """Build template context with current user."""
    ctx = base_context()
    user = get_current_user(request, db) if db else None
    ctx["current_user"] = user
    ctx["is_logged_in"] = user is not None
    if user:
        ctx["user_tier"] = user.tier
    return {**ctx, **extra}
