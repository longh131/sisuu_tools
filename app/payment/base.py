"""
Payment provider abstract base.
Future providers: Stripe, Paddle, Lemon Squeezy.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class CheckoutResult:
    """Result of a checkout session creation."""
    success: bool
    redirect_url: str
    session_id: str | None = None
    message: str = ""


@dataclass
class WebhookResult:
    """Result of webhook verification."""
    valid: bool
    event_type: str = ""
    plan_id: str = ""
    customer_email: str = ""


class PaymentProvider(ABC):
    """Abstract payment provider interface."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Provider identifier (stripe, paddle, stub)."""

    @abstractmethod
    async def create_checkout(self, plan_id: str, email: str = "") -> CheckoutResult:
        """Create a checkout session. Returns redirect URL."""

    @abstractmethod
    async def verify_webhook(self, payload: bytes, signature: str) -> WebhookResult:
        """Verify and parse a payment webhook."""

    def is_available(self) -> bool:
        """Whether real payments are enabled."""
        return False
