"""Launch statistics — email leads and tool usage analytics."""

from datetime import datetime, timedelta, timezone

from sqlalchemy import func

from app.database import SessionLocal
from app.models.email_lead import EmailLead
from app.models.usage_log import UsageLog
from app.utils.logger import get_logger

logger = get_logger("stats")


def _db_query(fn):
    """Run query with graceful fallback if DB unavailable."""
    try:
        db = SessionLocal()
        try:
            return fn(db)
        finally:
            db.close()
    except Exception as exc:
        logger.warning("Stats query failed: %s", exc)
        return None


def get_lead_stats() -> dict:
    """Email leads grouped by source."""
    def query(db):
        rows = (
            db.query(EmailLead.source, func.count(EmailLead.id))
            .group_by(EmailLead.source)
            .order_by(func.count(EmailLead.id).desc())
            .all()
        )
        total = db.query(func.count(EmailLead.id)).scalar() or 0
        today_start = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
        today = db.query(func.count(EmailLead.id)).filter(EmailLead.created_at >= today_start).scalar() or 0
        return {
            "total": total,
            "today": today,
            "by_source": [{"source": r[0] or "unknown", "count": r[1]} for r in rows],
        }

    return _db_query(query) or {"total": 0, "today": 0, "by_source": []}


def get_usage_stats(days: int = 30) -> dict:
    """Tool usage stats for the last N days."""
    since = datetime.now(timezone.utc) - timedelta(days=days)

    def query(db):
        total = db.query(func.count(UsageLog.id)).filter(UsageLog.created_at >= since).scalar() or 0
        today_start = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
        today = db.query(func.count(UsageLog.id)).filter(UsageLog.created_at >= today_start).scalar() or 0

        top_tools = (
            db.query(UsageLog.tool_slug, func.count(UsageLog.id).label("count"))
            .filter(UsageLog.created_at >= since)
            .group_by(UsageLog.tool_slug)
            .order_by(func.count(UsageLog.id).desc())
            .limit(10)
            .all()
        )

        by_tier = (
            db.query(UsageLog.tier, func.count(UsageLog.id))
            .filter(UsageLog.created_at >= since)
            .group_by(UsageLog.tier)
            .all()
        )

        return {
            "total": total,
            "today": today,
            "period_days": days,
            "top_tools": [{"slug": r[0], "count": r[1]} for r in top_tools],
            "by_tier": [{"tier": r[0], "count": r[1]} for r in by_tier],
        }

    return _db_query(query) or {"total": 0, "today": 0, "period_days": days, "top_tools": [], "by_tier": []}


def get_dashboard_stats() -> dict:
    """Combined stats for admin dashboard."""
    return {
        "leads": get_lead_stats(),
        "usage": get_usage_stats(),
    }
