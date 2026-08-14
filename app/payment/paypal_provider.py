"""PayPal payment provider — subscriptions for global sellers."""

import base64
import json

import httpx

from app.config import get_settings
from app.payment.base import CheckoutResult, PaymentProvider, WebhookResult
from app.utils.logger import get_logger

settings = get_settings()
logger = get_logger("paypal")

PLAN_ENV_KEYS = {"pro": "paypal_plan_pro", "business": "paypal_plan_business"}


class PayPalPaymentProvider(PaymentProvider):
    """PayPal Billing Subscriptions — no Stripe account required."""

    def __init__(self) -> None:
        self.mode = settings.paypal_mode
        self.base_url = (
            "https://api-m.paypal.com"
            if settings.paypal_is_live
            else "https://api-m.sandbox.paypal.com"
        )
        logger.info("PayPal provider initialized: mode=%s api=%s", self.mode, self.base_url)

    @property
    def name(self) -> str:
        return "paypal"

    def is_available(self) -> bool:
        return bool(
            settings.paypal_client_id
            and settings.paypal_client_secret
            and settings.paypal_plan_pro
            and settings.paypal_plan_business
        )

    def _plan_id(self, plan_id: str) -> str | None:
        key = PLAN_ENV_KEYS.get(plan_id)
        if not key:
            return None
        return getattr(settings, key, "") or None

    async def _access_token(self) -> str:
        creds = f"{settings.paypal_client_id}:{settings.paypal_client_secret}"
        encoded = base64.b64encode(creds.encode()).decode()
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.post(
                f"{self.base_url}/v1/oauth2/token",
                headers={
                    "Authorization": f"Basic {encoded}",
                    "Content-Type": "application/x-www-form-urlencoded",
                },
                data={"grant_type": "client_credentials"},
            )
            resp.raise_for_status()
            return resp.json()["access_token"]

    async def create_checkout(self, plan_id: str, email: str = "") -> CheckoutResult:
        paypal_plan = self._plan_id(plan_id)
        if not paypal_plan:
            return CheckoutResult(success=False, redirect_url="/pricing", message="Invalid plan.")

        token = await self._access_token()
        body: dict = {
            "plan_id": paypal_plan,
            "application_context": {
                "brand_name": settings.app_name,
                "locale": "en-US",
                "shipping_preference": "NO_SHIPPING",
                "user_action": "SUBSCRIBE_NOW",
                "return_url": f"{settings.site_url}/billing/success?provider=paypal",
                "cancel_url": f"{settings.site_url}/billing/cancel",
            },
        }
        if email:
            body["subscriber"] = {"email_address": email}

        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.post(
                f"{self.base_url}/v1/billing/subscriptions",
                headers={
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json",
                },
                json=body,
            )
            if resp.status_code >= 400:
                return CheckoutResult(
                    success=False,
                    redirect_url="/pricing",
                    message=f"PayPal error: {resp.text[:200]}",
                )
            data = resp.json()

        approve_url = next(
            (link["href"] for link in data.get("links", []) if link.get("rel") == "approve"),
            None,
        )
        if not approve_url:
            return CheckoutResult(success=False, redirect_url="/pricing", message="No PayPal approval URL.")

        return CheckoutResult(
            success=True,
            redirect_url=approve_url,
            session_id=data.get("id"),
        )

    async def verify_webhook(self, payload: bytes, signature: str) -> WebhookResult:
        """Parse PayPal webhook — signature verified when webhook_id configured."""
        try:
            event = json.loads(payload)
        except json.JSONDecodeError:
            return WebhookResult(valid=False)

        if settings.paypal_webhook_id and signature:
            if not await self._verify_webhook_signature(payload, signature):
                return WebhookResult(valid=False)

        event_type = event.get("event_type", "")
        resource = event.get("resource", {})

        if event_type == "BILLING.SUBSCRIPTION.ACTIVATED":
            plan_id = self._plan_from_paypal_plan(resource.get("plan_id", ""))
            email = resource.get("subscriber", {}).get("email_address", "")
            return WebhookResult(valid=True, event_type=event_type, plan_id=plan_id, customer_email=email)

        if event_type in ("BILLING.SUBSCRIPTION.CANCELLED", "BILLING.SUBSCRIPTION.SUSPENDED"):
            email = resource.get("subscriber", {}).get("email_address", "")
            return WebhookResult(
                valid=True,
                event_type="customer.subscription.deleted",
                plan_id="registered",
                customer_email=email,
            )

        return WebhookResult(valid=True, event_type=event_type)

    def _plan_from_paypal_plan(self, paypal_plan_id: str) -> str:
        if paypal_plan_id == settings.paypal_plan_business:
            return "business"
        if paypal_plan_id == settings.paypal_plan_pro:
            return "pro"
        return "pro"

    async def _verify_webhook_signature(self, payload: bytes, transmission_header: str) -> bool:
        """Verify via PayPal webhook signature API when headers passed as JSON."""
        try:
            headers = json.loads(transmission_header)
        except json.JSONDecodeError:
            return False

        token = await self._access_token()
        verify_body = {
            "auth_algo": headers.get("PAYPAL-AUTH-ALGO"),
            "cert_url": headers.get("PAYPAL-CERT-URL"),
            "transmission_id": headers.get("PAYPAL-TRANSMISSION-ID"),
            "transmission_sig": headers.get("PAYPAL-TRANSMISSION-SIG"),
            "transmission_time": headers.get("PAYPAL-TRANSMISSION-TIME"),
            "webhook_id": settings.paypal_webhook_id,
            "webhook_event": json.loads(payload),
        }
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.post(
                f"{self.base_url}/v1/notifications/verify-webhook-signature",
                headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
                json=verify_body,
            )
            if resp.status_code >= 400:
                return False
            return resp.json().get("verification_status") == "SUCCESS"
