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


def apply_webhook(db: Session, result: WebhookResult, stripe_sub_id: str = "") -> None:
    """Upgrade or downgrade user tier from Stripe webhook."""
    if not result.customer_email:
        logger.warning("Webhook missing customer email")
        return

    user = get_user_by_email(db, result.customer_email)
    if not user:
        logger.warning("No user for webhook email: %s", result.customer_email)
        return

    if result.event_type == "checkout.session.completed":
        update_user_tier(db, user, result.plan_id)
        sub = Subscription(
            user_id=user.id,
            plan_id=result.plan_id,
            status="active",
            stripe_subscription_id=stripe_sub_id or None,
        )
        db.add(sub)
        db.commit()
        logger.info("Upgraded user %s to %s", user.email, result.plan_id)

    elif result.event_type == "customer.subscription.deleted":
        update_user_tier(db, user, "registered")
        db.query(Subscription).filter(
            Subscription.user_id == user.id, Subscription.status == "active"
        ).update({"status": "canceled"})
        db.commit()
        logger.info("Downgraded user %s to registered", user.email)
