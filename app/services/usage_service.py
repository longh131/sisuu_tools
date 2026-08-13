"""Usage limit service — tracks AI tool usage per visitor/tier."""

import hashlib
from datetime import datetime, timezone

from fastapi import Request

from app.config import get_settings
from app.data.usage_limits import TIER_LIMITS
from app.database import SessionLocal
from app.models.usage_log import UsageLog
from app.utils.logger import get_logger

logger = get_logger("usage")
settings = get_settings()

SESSION_TIER_KEY = "user_tier"
SESSION_VISITOR_KEY = "visitor_id"


def get_visitor_id(request: Request) -> str:
    """Return stable visitor ID from session."""
    vid = request.session.get(SESSION_VISITOR_KEY)
    if not vid:
        raw = f"{request.client.host if request.client else 'unknown'}-{id(request.session)}"
        vid = hashlib.sha256(raw.encode()).hexdigest()[:32]
        request.session[SESSION_VISITOR_KEY] = vid
    return vid


def get_user_tier(request: Request) -> str:
    """Return current usage tier; refresh from DB when logged in."""
    user_id = request.session.get("user_id")
    if user_id:
        try:
            db = SessionLocal()
            try:
                from app.services.auth_service import get_user_by_id, sync_session_tier
                user = get_user_by_id(db, int(user_id))
                if user:
                    sync_session_tier(request, user)
                    return user.tier
            finally:
                db.close()
        except Exception:
            logger.warning("Tier refresh fallback — using session")
    return request.session.get(SESSION_TIER_KEY, "guest")


def set_user_tier(request: Request, tier: str) -> None:
    """Set user tier in session (e.g. after email subscribe → registered)."""
    if tier in TIER_LIMITS:
        request.session[SESSION_TIER_KEY] = tier


def get_daily_limit(tier: str) -> int:
    """Return daily AI limit for tier (-1 = unlimited)."""
    env_limits = {
        "guest": settings.guest_ai_daily_limit,
        "registered": settings.registered_ai_daily_limit,
    }
    if tier in env_limits:
        return env_limits[tier]
    return TIER_LIMITS.get(tier, TIER_LIMITS["guest"])


def count_today_usage(visitor_id: str) -> int:
    """Count AI tool uses today for a visitor."""
    today_start = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    try:
        db = SessionLocal()
        try:
            return (
                db.query(UsageLog)
                .filter(UsageLog.visitor_id == visitor_id)
                .filter(UsageLog.created_at >= today_start)
                .count()
            )
        finally:
            db.close()
    except Exception:
        logger.warning("Usage count fallback — DB unavailable")
        return 0


def check_ai_limit(request: Request) -> dict:
    """Check if visitor can use AI tool. Returns status dict."""
    tier = get_user_tier(request)
    limit = get_daily_limit(tier)
    visitor_id = get_visitor_id(request)
    used = count_today_usage(visitor_id)

    if limit == -1:
        return {"allowed": True, "tier": tier, "used": used, "limit": limit, "remaining": -1}

    remaining = max(0, limit - used)
    return {
        "allowed": used < limit,
        "tier": tier,
        "used": used,
        "limit": limit,
        "remaining": remaining,
    }


def record_ai_usage(request: Request, tool_slug: str) -> None:
    """Log one AI tool usage."""
    visitor_id = get_visitor_id(request)
    tier = get_user_tier(request)
    try:
        db = SessionLocal()
        try:
            db.add(UsageLog(visitor_id=visitor_id, tool_slug=tool_slug, tier=tier))
            db.commit()
        finally:
            db.close()
    except Exception:
        logger.warning("Failed to record usage for %s", tool_slug)


def limit_exceeded_message(status: dict) -> str:
    """Return user-friendly limit message."""
    if status["tier"] == "guest":
        return (
            f"Daily AI limit reached ({status['limit']} uses). "
            "Subscribe with your email for 10 free uses per day, or visit /pricing to upgrade."
        )
    return (
        f"Daily AI limit reached ({status['limit']} uses). "
        "Visit /pricing to upgrade to Pro for more."
    )
