"""
Payment provider factory.
V1.0 uses StubPaymentProvider — redirects to Contact for upgrade interest.
"""

from app.config import get_settings
from app.payment.base import CheckoutResult, PaymentProvider, WebhookResult

settings = get_settings()


class StubPaymentProvider(PaymentProvider):
    """
    Placeholder provider for V1.0 launch.
    Captures upgrade intent via Contact page — no real charges.
    """

    @property
    def name(self) -> str:
        return "stub"

    def is_available(self) -> bool:
        return False

    async def create_checkout(self, plan_id: str, email: str = "") -> CheckoutResult:
        """Redirect to contact form to capture upgrade interest."""
        valid_plans = ("pro", "business")
        plan = plan_id if plan_id in valid_plans else "pro"
        url = f"/contact?plan={plan}"
        if email:
            url += f"&email={email}"
        return CheckoutResult(
            success=True,
            redirect_url=url,
            message="Payments coming soon. Please leave your details and we will notify you.",
        )

    async def verify_webhook(self, payload: bytes, signature: str) -> WebhookResult:
        return WebhookResult(valid=False)


def get_payment_provider() -> PaymentProvider:
    """Return active payment provider. Extend when Stripe/Paddle is added."""
    provider_name = getattr(settings, "payment_provider", "stub")
    if provider_name == "stub":
        return StubPaymentProvider()
    # Future: elif provider_name == "stripe": return StripeProvider()
    return StubPaymentProvider()
