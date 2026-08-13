"""Admin lists — leads, payments."""

from sqlalchemy.orm import Session

from app.models.email_lead import EmailLead
from app.models.payment import Payment
from app.models.user import User


def list_leads(db: Session, limit: int = 200) -> list[dict]:
    rows = db.query(EmailLead).order_by(EmailLead.created_at.desc()).limit(limit).all()
    return [
        {
            "id": r.id,
            "email": r.email,
            "source": r.source or "—",
            "status": r.status,
            "created_at": r.created_at.strftime("%Y-%m-%d %H:%M") if r.created_at else "",
        }
        for r in rows
    ]


def list_payments(db: Session, limit: int = 100) -> list[dict]:
    rows = (
        db.query(Payment, User.email)
        .outerjoin(User, Payment.user_id == User.id)
        .order_by(Payment.created_at.desc())
        .limit(limit)
        .all()
    )
    return [
        {
            "id": p.id,
            "email": email or "—",
            "plan_id": p.plan_id,
            "amount_cents": p.amount_cents,
            "currency": p.currency,
            "status": p.status,
            "session_id": p.stripe_checkout_session_id or "—",
            "created_at": p.created_at.strftime("%Y-%m-%d %H:%M") if p.created_at else "",
        }
        for p, email in rows
    ]
