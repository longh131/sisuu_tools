"""
Contact form handling — validation and message logging.
"""

import re
from datetime import datetime, timezone
from pathlib import Path

from app.config import get_settings
from app.utils.logger import get_logger

logger = get_logger("contact")

EMAIL_PATTERN = re.compile(r"^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$")
VALID_SUBJECTS = {"general", "tool", "bug", "partnership", "other"}


def validate_contact_form(name: str, email: str, subject: str, message: str) -> str | None:
    """Validate contact form fields. Returns error message or None if valid."""
    name = (name or "").strip()
    email = (email or "").strip()
    subject = (subject or "").strip()
    message = (message or "").strip()

    if not name or len(name) < 2:
        return "Please enter your name (at least 2 characters)."
    if len(name) > 100:
        return "Name is too long (maximum 100 characters)."
    if not email or not EMAIL_PATTERN.match(email):
        return "Please enter a valid email address."
    if subject not in VALID_SUBJECTS:
        return "Please select a valid subject."
    if not message or len(message) < 10:
        return "Please enter a message (at least 10 characters)."
    if len(message) > 2000:
        return "Message is too long (maximum 2000 characters)."
    return None


def save_contact_message(name: str, email: str, subject: str, message: str) -> None:
    """Log contact message to file for admin review."""
    settings = get_settings()
    log_dir = Path(settings.log_dir)
    log_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    entry = (
        f"\n--- Contact Message [{timestamp}] ---\n"
        f"Name: {name}\nEmail: {email}\nSubject: {subject}\n"
        f"Message:\n{message}\n"
    )

    log_file = log_dir / "contact_messages.log"
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(entry)

    logger.info("Contact message received from %s <%s> [%s]", name, email, subject)
