"""Static content pages — Sprint 7 full pages."""

from fastapi import APIRouter, Depends, Form, Query, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.data.pricing_plans import PRICING_FAQ, PRICING_PAGE, PRICING_PLANS
from app.data.static_pages import ABOUT_PAGE, CONTACT_PAGE, PRIVACY_PAGE, TERMS_PAGE
from app.payment import get_payment_provider
from app.services.contact_service import save_contact_message, validate_contact_form
from app.services.tools_service import search_tools
from app.utils.seo import breadcrumb_schema, faq_schema
from app.utils.templates import base_context, templates

router = APIRouter(tags=["pages"])


def _static_context(page_meta: dict, **extra) -> dict:
    """Build template context for static pages with SEO and breadcrumb."""
    ctx = base_context()
    crumbs = page_meta.get("breadcrumb", [])
    return {
        **ctx,
        "page_title": page_meta["title"],
        "page_description": page_meta["description"],
        "canonical_url": ctx["site_url"] + "/" + extra.get("slug", ""),
        "page_h1": page_meta["h1"],
        "breadcrumbs": crumbs,
        "schema_breadcrumb": breadcrumb_schema(crumbs, ctx["site_url"]),
        "last_updated": page_meta.get("last_updated"),
        **extra,
    }


@router.get("/about", response_class=HTMLResponse)
async def about(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        request=request, name="about.html",
        context=_static_context(ABOUT_PAGE, slug="about"),
    )


@router.get("/contact", response_class=HTMLResponse)
async def contact_page(
    request: Request,
    plan: str | None = Query(None),
    email: str | None = Query(None),
) -> HTMLResponse:
    """Contact page with optional plan prefill from Pricing upgrade."""
    prefill: dict = {}
    if plan in ("pro", "business"):
        prefill["subject"] = plan
        prefill["message"] = f"I am interested in the {plan.title()} plan. Please notify me when it launches."
    if email:
        prefill["email"] = email
    return templates.TemplateResponse(
        request=request, name="contact.html",
        context={
            **_static_context(CONTACT_PAGE, slug="contact"),
            "success": False, "error": None, "form": prefill,
            "plan_interest": plan,
        },
    )


@router.post("/contact", response_class=HTMLResponse)
async def contact_submit(
    request: Request,
    name: str = Form(""),
    email: str = Form(""),
    subject: str = Form(""),
    message: str = Form(""),
) -> HTMLResponse:
    """Handle contact form submission with validation."""
    form_data = {"name": name, "email": email, "subject": subject, "message": message}
    error = validate_contact_form(name, email, subject, message)

    base = _static_context(CONTACT_PAGE, slug="contact")

    if error:
        return templates.TemplateResponse(
            request=request, name="contact.html",
            context={**base, "success": False, "error": error, "form": form_data},
            status_code=400,
        )

    save_contact_message(name.strip(), email.strip(), subject.strip(), message.strip())
    return templates.TemplateResponse(
        request=request, name="contact.html",
        context={**base, "success": True, "error": None, "form": {}},
    )


@router.get("/privacy", response_class=HTMLResponse)
async def privacy(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        request=request, name="privacy.html",
        context=_static_context(PRIVACY_PAGE, slug="privacy"),
    )


@router.get("/terms", response_class=HTMLResponse)
async def terms(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        request=request, name="terms.html",
        context=_static_context(TERMS_PAGE, slug="terms"),
    )


# ── Pricing (commercial Phase 1) ──

@router.get("/pricing", response_class=HTMLResponse)
async def pricing(request: Request) -> HTMLResponse:
    crumbs = PRICING_PAGE.get("breadcrumb", [])
    ctx = _static_context(PRICING_PAGE, slug="pricing")
    provider = get_payment_provider()
    payments_enabled = provider.is_available()
    plans = []
    for plan in PRICING_PLANS:
        p = dict(plan)
        if payments_enabled and p["id"] in ("pro", "business"):
            p["coming_soon"] = False
            p["cta_checkout"] = True
        plans.append(p)
    return templates.TemplateResponse(
        request=request, name="pricing.html",
        context={
            **ctx,
            "plans": plans,
            "payments_enabled": payments_enabled,
            "faq_items": PRICING_FAQ,
            "schema_faq": faq_schema(PRICING_FAQ),
            "schema_breadcrumb": breadcrumb_schema(crumbs, ctx["site_url"]),
        },
    )


@router.get("/policy", response_class=HTMLResponse)
async def policy_page(request: Request) -> HTMLResponse:
    ctx = base_context()
    return templates.TemplateResponse(request=request, name="page.html", context={
        **ctx, "page_title": "Policy Center — Seller Toolkit",
        "page_description": "Platform policies for Amazon, eBay, Walmart and TikTok Shop sellers.",
        "canonical_url": ctx["site_url"] + "/policy", "page_h1": "Policy Center",
        "page_content": '<p><a href="/tools/policy">Browse Policy Tools</a></p>',
    })


@router.get("/resources")
async def resources() -> RedirectResponse:
    return RedirectResponse(url="/tools/seller-resources", status_code=301)


@router.get("/search", response_class=HTMLResponse)
async def search(request: Request, q: str | None = Query(None), db: Session = Depends(get_db)) -> HTMLResponse:
    from app.routes.tools import _render_tools_page
    return _render_tools_page(
        request, db,
        page_h1="Search Results" if q else "Search Tools",
        page_intro=f'Showing results for "{q}"' if q else "Enter a keyword to find seller tools.",
        tools=search_tools(q or "", db),
        page=1,
        page_title=f"Search: {q or 'Tools'} — Seller Toolkit",
    )
