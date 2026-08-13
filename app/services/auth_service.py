"""User authentication service — register, login, session."""

import re

import bcrypt
from fastapi import Request
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.user import User
from app.utils.logger import get_logger

logger = get_logger("auth")

SESSION_USER_ID = "user_id"
EMAIL_RE = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(plain: str, hashed: str) -> bool:
    try:
        return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))
    except (ValueError, TypeError):
        return False


def validate_email(email: str) -> bool:
    return bool(email and EMAIL_RE.match(email.strip()))


def validate_password(password: str) -> str | None:
    if not password or len(password) < 8:
        return "Password must be at least 8 characters."
    return None


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email.strip().lower()).first()


def get_user_by_id(db: Session, user_id: int) -> User | None:
    return db.query(User).filter(User.id == user_id, User.is_active == True).first()  # noqa: E712


def register_user(db: Session, email: str, password: str) -> tuple[User | None, str | None]:
    """Create account. Returns (user, error_message)."""
    email = email.strip().lower()
    if not validate_email(email):
        return None, "Invalid email address."
    err = validate_password(password)
    if err:
        return None, err
    if get_user_by_email(db, email):
        return None, "An account with this email already exists."

    user = User(
        email=email,
        password_hash=hash_password(password),
        tier="registered",
    )
    try:
        db.add(user)
        db.commit()
        db.refresh(user)
    except SQLAlchemyError as exc:
        db.rollback()
        logger.exception("Register failed for %s", email)
        msg = str(exc).lower()
        if "users" in msg and ("doesn't exist" in msg or "1146" in msg):
            return None, "Registration unavailable — database migration pending. Contact support."
        return None, "Registration failed. Please try again later."
    return user, None


def authenticate_user(db: Session, email: str, password: str) -> User | None:
    user = get_user_by_email(db, email)
    if not user or not user.is_active:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user


def login_user(request: Request, user: User) -> None:
    """Store user in session and sync tier."""
    request.session[SESSION_USER_ID] = user.id
    request.session["user_tier"] = user.tier


def logout_user(request: Request) -> None:
    request.session.pop(SESSION_USER_ID, None)
    request.session["user_tier"] = "guest"


def get_current_user(request: Request, db: Session | None = None) -> User | None:
    """Return logged-in user or None."""
    user_id = request.session.get(SESSION_USER_ID)
    if not user_id or not db:
        return None
    return get_user_by_id(db, int(user_id))


def sync_session_tier(request: Request, user: User) -> None:
    """Refresh session tier from DB (after payment upgrade)."""
    request.session["user_tier"] = user.tier


def update_user_tier(db: Session, user: User, tier: str) -> User:
    user.tier = tier
    db.commit()
    db.refresh(user)
    return user
