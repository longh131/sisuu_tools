"""Homepage route — full MVP homepage per docs/04-首页开发.md."""

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from app.data.homepage_data import (
    FAQ_ITEMS,
    HERO_PREVIEW_ITEMS,
    HERO_PREVIEW_RESULT,
    HERO_TRUST,
    LATEST_TOOLS,
    POPULAR_TOOLS,
    TOOL_CATEGORIES,
    WHY_CHOOSE_ITEMS,
)
from app.utils.templates import base_context, templates

router = APIRouter(tags=["home"])

HOME_TITLE = "Seller Toolkit — Free Tools for Amazon, eBay & Shopify Sellers"
HOME_DESCRIPTION = (
    "Free seller tools for Amazon, eBay, Shopify, Walmart and TikTok Shop. "
    "Calculators, AI tools, policy center and seller resources — no registration required."
)


@router.get("/", response_class=HTMLResponse, name="home")
async def index(request: Request) -> HTMLResponse:
    """Render the full homepage with all MVP sections."""
    ctx = base_context()
    context = {
        **ctx,
        "page_title": HOME_TITLE,
        "page_description": HOME_DESCRIPTION,
        "canonical_url": ctx["site_url"] + "/",
        "popular_tools": POPULAR_TOOLS,
        "latest_tools": LATEST_TOOLS,
        "tool_categories": TOOL_CATEGORIES,
        "why_choose_items": WHY_CHOOSE_ITEMS,
        "faq_items": FAQ_ITEMS,
        "hero_trust": HERO_TRUST,
        "hero_preview_items": HERO_PREVIEW_ITEMS,
        "hero_preview_result": HERO_PREVIEW_RESULT,
    }
    return templates.TemplateResponse(request=request, name="index.html", context=context)
