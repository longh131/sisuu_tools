"""Admin user management service."""

from sqlalchemy.orm import Session

from app.models.subscription import Subscription
from app.models.user import User
from app.services.auth_service import update_user_tier


def list_users(db: Session, limit: int = 200) -> list[dict]:
    rows = db.query(User).order_by(User.created_at.desc()).limit(limit).all()
    return [
        {
            "id": u.id,
            "email": u.email,
            "tier": u.tier,
            "is_active": u.is_active,
            "created_at": u.created_at.strftime("%Y-%m-%d %H:%M") if u.created_at else "",
        }
        for u in rows
    ]


def get_user(db: Session, user_id: int) -> User | None:
    return db.query(User).filter(User.id == user_id).first()


def set_user_tier_admin(db: Session, user: User, tier: str) -> User:
    valid = ("guest", "registered", "pro", "business")
    if tier not in valid:
        tier = "registered"
    return update_user_tier(db, user, tier)


def toggle_user_active(db: Session, user: User, active: bool) -> User:
    user.is_active = active
    db.commit()
    db.refresh(user)
    return user


def list_subscriptions(db: Session, limit: int = 100) -> list[dict]:
    rows = (
        db.query(Subscription, User.email)
        .join(User, Subscription.user_id == User.id)
        .order_by(Subscription.created_at.desc())
        .limit(limit)
        .all()
    )
    return [
        {
            "id": s.id,
            "email": email,
            "plan_id": s.plan_id,
            "status": s.status,
            "stripe_subscription_id": s.stripe_subscription_id or "—",
            "created_at": s.created_at.strftime("%Y-%m-%d") if s.created_at else "",
        }
        for s, email in rows
    ]
