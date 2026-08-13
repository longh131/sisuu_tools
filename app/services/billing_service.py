"""Billing service — checkout and webhook handling."""

from sqlalchemy.orm import Session

from app.models.payment import Payment
from app.models.subscription import Subscription
from app.models.user import User
from app.payment.base import WebhookResult
from app.services.auth_service import get_user_by_email, update_user_tier
from app.utils.logger import get_logger

logger = get_logger("billing")

PLAN_AMOUNTS = {"pro": 1900, "business": 4900}


def record_payment(db: Session, user_id: int | None, plan_id: str, session_id: str, status: str) -> None:
    db.add(Payment(
        user_id=user_id,
        plan_id=plan_id,
        amount_cents=PLAN_AMOUNTS.get(plan_id, 0),
        status=status,
        stripe_checkout_session_id=session_id,
    ))
    db.commit()


def activate_subscription_from_return(db: Session, user: User, subscription_id: str) -> bool:
    """Activate tier when user returns from PayPal success URL (fallback if webhook email mismatches)."""
    if not subscription_id:
        return False

    pending = (
        db.query(Payment)
        .filter(
            Payment.user_id == user.id,
            Payment.stripe_checkout_session_id == subscription_id,
            Payment.status == "pending",
        )
        .first()
    )
    if not pending:
        # Fallback: latest pending payment for this user
        pending = (
            db.query(Payment)
            .filter(Payment.user_id == user.id, Payment.status == "pending")
            .order_by(Payment.created_at.desc())
            .first()
        )
    if not pending:
        return False

    existing = (
        db.query(Subscription)
        .filter(Subscription.user_id == user.id, Subscription.status == "active")
        .first()
    )
    if existing and user.tier == pending.plan_id:
        pending.status = "completed"
        db.commit()
        return True

    update_user_tier(db, user, pending.plan_id)
    if not existing:
        db.add(Subscription(
            user_id=user.id,
            plan_id=pending.plan_id,
            status="active",
            stripe_subscription_id=subscription_id,
        ))
    pending.status = "completed"
    if subscription_id:
        pending.stripe_checkout_session_id = subscription_id
    db.commit()
    logger.info("Activated %s -> %s via return URL sub=%s", user.email, pending.plan_id, subscription_id)
    return True


def apply_webhook(db: Session, result: WebhookResult, external_sub_id: str = "") -> None:
    """Upgrade or downgrade user tier from payment webhook."""
    user = None
    if result.customer_email:
        user = get_user_by_email(db, result.customer_email)

    # PayPal buyer email may differ from site account — match pending payment by subscription id
    if not user and external_sub_id:
        pending = (
            db.query(Payment)
            .filter(Payment.stripe_checkout_session_id == external_sub_id, Payment.status == "pending")
            .first()
        )
        if pending and pending.user_id:
            user = db.query(User).filter(User.id == pending.user_id).first()

    if not user:
        logger.warning(
            "No user for webhook email=%s sub_id=%s",
            result.customer_email or "—",
            external_sub_id or "—",
        )
        return

    activated_events = (
        "checkout.session.completed",           # Stripe
        "BILLING.SUBSCRIPTION.ACTIVATED",     # PayPal
    )

    if result.event_type in activated_events:
        update_user_tier(db, user, result.plan_id)
        sub_id = external_sub_id or None
        sub = Subscription(
            user_id=user.id,
            plan_id=result.plan_id,
            status="active",
            stripe_subscription_id=sub_id,
        )
        db.add(sub)
        # Mark latest pending payment as completed
        pending = (
            db.query(Payment)
            .filter(Payment.user_id == user.id, Payment.plan_id == result.plan_id, Payment.status == "pending")
            .order_by(Payment.created_at.desc())
            .first()
        )
        if pending:
            pending.status = "completed"
            if sub_id and not pending.stripe_checkout_session_id:
                pending.stripe_checkout_session_id = sub_id
        db.commit()
        logger.info("Upgraded user %s to %s via %s", user.email, result.plan_id, result.event_type)

    elif result.event_type == "customer.subscription.deleted":
        update_user_tier(db, user, "registered")
        db.query(Subscription).filter(
            Subscription.user_id == user.id, Subscription.status == "active"
        ).update({"status": "canceled"})
        db.commit()
        logger.info("Downgraded user %s to registered", user.email)
