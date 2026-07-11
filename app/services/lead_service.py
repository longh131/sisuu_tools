"""Lead capture service — email collection for commercial funnel."""

import re

from sqlalchemy.exc import IntegrityError

from app.database import SessionLocal
from app.models.email_lead import EmailLead
from app.utils.logger import get_logger

logger = get_logger("leads")

EMAIL_PATTERN = re.compile(r"^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$")
VALID_SOURCES = {"hero", "footer", "tool_result", "pricing", "pricing_pro", "pricing_business", "popup", "other"}


def validate_email(email: str) -> str | None:
    """Validate email. Returns error message or None."""
    email = (email or "").strip().lower()
    if not email or not EMAIL_PATTERN.match(email):
        return "Please enter a valid email address."
    if len(email) > 255:
        return "Email is too long."
    return None


def save_lead(email: str, source: str = "other") -> tuple[bool, str]:
    """Save email lead. Returns (success, message)."""
    email = email.strip().lower()
    source = source if source in VALID_SOURCES else "other"

    try:
        db = SessionLocal()
        try:
            existing = db.query(EmailLead).filter(EmailLead.email == email).first()
            if existing:
                return True, "You are already subscribed. Thank you!"

            db.add(EmailLead(email=email, source=source))
            db.commit()
            logger.info("New lead: %s [%s]", email, source)
            return True, "Thank you! You now have 10 free AI uses per day."
        finally:
            db.close()
    except IntegrityError:
        return True, "You are already subscribed. Thank you!"
    except Exception as exc:
        logger.error("Lead save failed: %s", exc)
        # Graceful fallback — still upgrade tier in session
        return True, "Thank you! Check your inbox for seller tips."
