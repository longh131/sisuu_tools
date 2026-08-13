"""Billing routes — Stripe checkout and webhooks."""

import json

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.payment import get_payment_provider
from app.services.auth_service import get_current_user
from app.services.billing_service import apply_webhook, record_payment
from app.utils.page_context import page_context
from app.utils.templates import templates

router = APIRouter(tags=["billing"])


class CheckoutBody(BaseModel):
    plan_id: str


@router.post("/api/billing/checkout")
async def create_checkout(request: Request, body: CheckoutBody, db: Session = Depends(get_db)):
    """Create payment checkout session."""
    plan_id = body.plan_id
    if plan_id not in ("pro", "business"):
        raise HTTPException(status_code=400, detail="Invalid plan")

    user = get_current_user(request, db)
    if not user:
        raise HTTPException(status_code=401, detail="Please sign in before upgrading. Create a free account first.")

    email = user.email
    provider = get_payment_provider()
    result = await provider.create_checkout(plan_id, email=email)

    if not result.success:
        raise HTTPException(status_code=400, detail=result.message or "Checkout failed")

    if result.session_id and user:
        record_payment(db, user.id, plan_id, result.session_id, "pending")

    return {"redirect_url": result.redirect_url}


@router.post("/api/billing/webhook")
async def payment_webhook(request: Request, db: Session = Depends(get_db)):
    """Payment webhook — Stripe or PayPal depending on provider."""
    payload = await request.body()
    provider = get_payment_provider()

    if provider.name == "paypal":
        paypal_headers = json.dumps({
            "PAYPAL-AUTH-ALGO": request.headers.get("PAYPAL-AUTH-ALGO", ""),
            "PAYPAL-CERT-URL": request.headers.get("PAYPAL-CERT-URL", ""),
            "PAYPAL-TRANSMISSION-ID": request.headers.get("PAYPAL-TRANSMISSION-ID", ""),
            "PAYPAL-TRANSMISSION-SIG": request.headers.get("PAYPAL-TRANSMISSION-SIG", ""),
            "PAYPAL-TRANSMISSION-TIME": request.headers.get("PAYPAL-TRANSMISSION-TIME", ""),
        })
        signature = paypal_headers
    else:
        signature = request.headers.get("stripe-signature", "")

    result = await provider.verify_webhook(payload, signature)
    if not result.valid:
        raise HTTPException(status_code=400, detail="Invalid webhook")

    apply_webhook(db, result)
    return {"received": True}


@router.get("/billing/success", response_class=HTMLResponse)
async def billing_success(request: Request, db: Session = Depends(get_db)) -> HTMLResponse:
    ctx = page_context(request, db, page_title="Payment Successful")
    return templates.TemplateResponse(request=request, name="billing/success.html", context=ctx)


@router.get("/billing/cancel", response_class=HTMLResponse)
async def billing_cancel(request: Request, db: Session = Depends(get_db)) -> HTMLResponse:
    ctx = page_context(request, db, page_title="Payment Cancelled")
    return templates.TemplateResponse(request=request, name="billing/cancel.html", context=ctx)
