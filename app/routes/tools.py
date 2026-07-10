"""Tool Center and tool detail routes — Sprint 3."""

from fastapi import APIRouter, HTTPException, Query, Request
from fastapi.responses import HTMLResponse

from app.services.tools_service import (
    get_all_categories,
    get_all_tools,
    get_category,
    get_category_faqs,
    get_popular_tools_list,
    get_related_tools,
    get_tool_by_slug,
    get_tool_page_config,
    get_tools_by_category,
    is_category_slug,
    is_tool_slug,
    paginate_tools,
    search_tools,
)
from app.utils.seo import breadcrumb_schema, faq_schema, software_app_schema
from app.utils.templates import base_context, templates

router = APIRouter(tags=["tools"])

TOOLS_TITLE = "Seller Tools — Free eCommerce Tools for Amazon & eBay Sellers"
TOOLS_DESCRIPTION = (
    "Browse free seller tools including AI tools, calculators, policy center "
    "and seller resources for Amazon, eBay, Shopify and Walmart sellers."
)


def _category_url(category: str | None, page: int = 1) -> str:
    """Build canonical URL for category page."""
    if not category:
        return "/tools" if page == 1 else f"/tools/page/{page}"
    return f"/tools/{category}" if page == 1 else f"/tools/{category}/page/{page}"


def _render_tools_page(
    request: Request,
    *,
    page_h1: str,
    page_intro: str,
    tools: list[dict],
    page: int,
    active_category: str | None = None,
    page_title: str = TOOLS_TITLE,
    page_description: str = TOOLS_DESCRIPTION,
) -> HTMLResponse:
    """Render unified Tool Center template."""
    ctx = base_context()
    pagination = paginate_tools(tools, page)
    canonical = _category_url(active_category, page)
    faqs = get_category_faqs(active_category)
    related = get_popular_tools_list(limit=6)

    context = {
        **ctx,
        "page_title": page_title,
        "page_description": page_description,
        "canonical_url": ctx["site_url"] + canonical,
        "page_h1": page_h1,
        "page_intro": page_intro,
        "tools": pagination["items"],
        "pagination": pagination,
        "categories": get_all_categories(),
        "active_category": active_category,
        "faqs": faqs,
        "related_tools": related,
        "breadcrumbs": _breadcrumbs(active_category, page_h1),
        "schema_faq": faq_schema(faqs),
        "schema_breadcrumb": breadcrumb_schema(_breadcrumbs(active_category, page_h1), ctx["site_url"]),
    }
    return templates.TemplateResponse(request=request, name="tools.html", context=context)


def _breadcrumbs(category: str | None, title: str) -> list[dict]:
    crumbs = [{"name": "Home", "url": "/"}, {"name": "Tools", "url": "/tools"}]
    if category:
        cat = get_category(category)
        crumbs.append({"name": cat["name"], "url": f"/tools/{category}"})
    else:
        crumbs.append({"name": title, "url": ""})
    return crumbs


@router.get("/tools", response_class=HTMLResponse, name="tools")
async def tools_all(request: Request) -> HTMLResponse:
    return _render_tools_page(
        request,
        page_h1="Seller Tools",
        page_intro=(
            "Free tools for Amazon, eBay, Shopify, Walmart and TikTok Shop sellers. "
            "Browse AI tools, calculators, policy center and seller resources."
        ),
        tools=get_all_tools(),
        page=1,
    )


@router.get("/tools/page/{page_num:int}", response_class=HTMLResponse)
async def tools_all_paged(request: Request, page_num: int) -> HTMLResponse:
    return _render_tools_page(
        request,
        page_h1="Seller Tools",
        page_intro="Free tools for global eCommerce sellers.",
        tools=get_all_tools(),
        page=page_num,
        page_title=f"Seller Tools — Page {page_num}",
    )


@router.get("/tools/{slug}/page/{page_num:int}", response_class=HTMLResponse)
async def category_paged(request: Request, slug: str, page_num: int) -> HTMLResponse:
    if not is_category_slug(slug):
        raise HTTPException(status_code=404, detail="Category not found")
    cat = get_category(slug)
    return _render_tools_page(
        request,
        page_h1=cat["name"],
        page_intro=cat["description"],
        tools=get_tools_by_category(slug),
        page=page_num,
        active_category=slug,
        page_title=f"{cat['name']} — {TOOLS_TITLE}",
        page_description=cat["description"],
    )


@router.get("/tools/{slug}", response_class=HTMLResponse, name="tool_or_category")
async def tool_or_category(request: Request, slug: str) -> HTMLResponse:
    # Category page
    if is_category_slug(slug):
        cat = get_category(slug)
        return _render_tools_page(
            request,
            page_h1=cat["name"],
            page_intro=cat["description"],
            tools=get_tools_by_category(slug),
            page=1,
            active_category=slug,
            page_title=f"{cat['name']} — {TOOLS_TITLE}",
            page_description=cat["description"],
        )

    # Tool detail page
    tool = get_tool_by_slug(slug)
    if not tool:
        raise HTTPException(status_code=404, detail="Not found")

    config = get_tool_page_config(slug)
    ctx = base_context()
    cat = get_category(tool.get("category", ""))
    context = {
        **ctx,
        "page_title": f"{tool['name']} — Free Online Tool | {ctx['app_name']}",
        "page_description": tool.get("intro") or tool.get("description", ""),
        "canonical_url": ctx["site_url"] + f"/tools/{slug}",
        "tool": tool,
        "config": config,
        "faqs": config.get("faqs", []),
        "related_tools": get_related_tools(slug),
        "breadcrumbs": [
            {"name": "Home", "url": "/"},
            {"name": "Tools", "url": "/tools"},
            {"name": cat["name"] if cat else "Tools", "url": f"/tools/{tool.get('category', '')}"},
            {"name": tool["name"], "url": ""},
        ],
        "schema_software": software_app_schema(tool, ctx["site_url"]),
        "schema_faq": faq_schema(config.get("faqs", [])),
        "schema_breadcrumb": breadcrumb_schema([
            {"name": "Home", "url": "/"},
            {"name": "Tools", "url": "/tools"},
            {"name": cat["name"] if cat else "Tools", "url": f"/tools/{tool.get('category', '')}"},
            {"name": tool["name"], "url": ""},
        ], ctx["site_url"]),
    }
    return templates.TemplateResponse(request=request, name="tool.html", context=context)
