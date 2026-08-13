"""Stripe payment provider — V1.1."""

import stripe

from app.config import get_settings
from app.payment.base import CheckoutResult, PaymentProvider, WebhookResult

settings = get_settings()


class StripePaymentProvider(PaymentProvider):
    """Stripe Checkout subscriptions for Pro / Business plans."""

    PLAN_PRICES = {
        "pro": "stripe_price_pro",
        "business": "stripe_price_business",
    }

    def __init__(self) -> None:
        stripe.api_key = settings.stripe_secret_key

    @property
    def name(self) -> str:
        return "stripe"

    def is_available(self) -> bool:
        return bool(
            settings.stripe_secret_key
            and settings.stripe_price_pro
            and settings.stripe_price_business
        )

    def _price_id(self, plan_id: str) -> str | None:
        key = self.PLAN_PRICES.get(plan_id)
        if not key:
            return None
        return getattr(settings, key, "")

    async def create_checkout(self, plan_id: str, email: str = "") -> CheckoutResult:
        price_id = self._price_id(plan_id)
        if not price_id:
            return CheckoutResult(success=False, redirect_url="/pricing", message="Invalid plan.")

        session_kwargs: dict = {
            "mode": "subscription",
            "line_items": [{"price": price_id, "quantity": 1}],
            "success_url": f"{settings.site_url}/billing/success?session_id={{CHECKOUT_SESSION_ID}}",
            "cancel_url": f"{settings.site_url}/billing/cancel",
            "metadata": {"plan_id": plan_id},
        }
        if email:
            session_kwargs["customer_email"] = email

        session = stripe.checkout.Session.create(**session_kwargs)
        return CheckoutResult(
            success=True,
            redirect_url=session.url or "/pricing",
            session_id=session.id,
        )

    async def verify_webhook(self, payload: bytes, signature: str) -> WebhookResult:
        try:
            event = stripe.Webhook.construct_event(
                payload, signature, settings.stripe_webhook_secret
            )
        except Exception:
            return WebhookResult(valid=False)

        data = event.get("data", {}).get("object", {})
        event_type = event.get("type", "")

        if event_type == "checkout.session.completed":
            plan_id = (data.get("metadata") or {}).get("plan_id", "pro")
            email = data.get("customer_details", {}).get("email") or data.get("customer_email", "")
            return WebhookResult(valid=True, event_type=event_type, plan_id=plan_id, customer_email=email)

        if event_type == "customer.subscription.deleted":
            email = data.get("customer_email", "")
            return WebhookResult(valid=True, event_type=event_type, plan_id="registered", customer_email=email)

        return WebhookResult(valid=True, event_type=event_type)
