"""
Unified tools data service.
Reads from database when available, falls back to seed data.
"""

import math

from sqlalchemy.orm import Session

from app.data.seed_tools import SEED_TOOLS, TOOLS_PER_PAGE, get_latest_tools, get_popular_tools
from app.data.tool_categories import CATEGORY_TAB_ORDER, TOOL_CATEGORIES
from app.data.category_faqs import CATEGORY_FAQS
from app.data.tool_configs import TOOL_CONFIGS, get_default_config, get_tool_config


def _tool_from_db(row) -> dict:
    """Convert ORM Tool + category to dict."""
    return {
        "id": row.id,
        "name": row.name,
        "slug": row.slug,
        "description": row.description or "",
        "intro": row.intro or row.description or "",
        "icon": row.icon or "wrench",
        "category": row.category.slug if row.category else "",
        "category_name": row.category.name if row.category else "",
        "is_ai": row.is_ai,
        "is_popular": getattr(row, "is_popular", False),
        "is_featured": getattr(row, "is_featured", False),
        "sort_order": getattr(row, "sort_order", 99),
        "status": row.status,
    }


def _load_tools(db: Session | None = None) -> list[dict]:
    """Load tools from DB or seed."""
    if db:
        try:
            from app.models.tool import Tool
            rows = db.query(Tool).filter(Tool.status == True).all()  # noqa: E712
            if rows:
                return [_tool_from_db(r) for r in rows]
        except Exception:
            pass
    return list(SEED_TOOLS)


def get_all_tools(db: Session | None = None) -> list[dict]:
    """Return all active tools sorted: featured > popular > sort_order."""
    tools = _load_tools(db)
    return sorted(tools, key=lambda t: (
        not t.get("is_featured", False),
        not t.get("is_popular", False),
        t.get("sort_order", 99),
        t.get("name", ""),
    ))


def get_tool_by_slug(slug: str, db: Session | None = None) -> dict | None:
    """Find tool by slug."""
    for tool in _load_tools(db):
        if tool["slug"] == slug:
            return tool
    return None


def get_tools_by_category(category_slug: str | None, db: Session | None = None) -> list[dict]:
    """Filter tools by category."""
    tools = get_all_tools(db)
    if not category_slug:
        return tools
    return [t for t in tools if t.get("category") == category_slug]


def search_tools(query: str, db: Session | None = None) -> list[dict]:
    """Search tools by keyword."""
    if not query or not query.strip():
        return get_all_tools(db)
    q = query.strip().lower()
    results = []
    for tool in _load_tools(db):
        searchable = " ".join([
            tool.get("name", ""),
            tool.get("description", ""),
            tool.get("category", ""),
            tool.get("slug", "").replace("-", " "),
        ]).lower()
        if q in searchable:
            results.append(tool)
    return sorted(results, key=lambda t: t.get("sort_order", 99))


def get_category(slug: str) -> dict | None:
    return TOOL_CATEGORIES.get(slug)


def get_all_categories() -> list[dict]:
    return [TOOL_CATEGORIES[s] for s in CATEGORY_TAB_ORDER if s in TOOL_CATEGORIES]


def is_category_slug(slug: str) -> bool:
    return slug in TOOL_CATEGORIES


def is_tool_slug(slug: str, db: Session | None = None) -> bool:
    return get_tool_by_slug(slug, db) is not None


def paginate_tools(tools: list[dict], page: int = 1, per_page: int = TOOLS_PER_PAGE) -> dict:
    """Paginate tool list. Returns page data dict."""
    page = max(1, page)
    total = len(tools)
    total_pages = max(1, math.ceil(total / per_page))
    page = min(page, total_pages)
    start = (page - 1) * per_page
    end = start + per_page
    return {
        "items": tools[start:end],
        "page": page,
        "per_page": per_page,
        "total": total,
        "total_pages": total_pages,
        "has_prev": page > 1,
        "has_next": page < total_pages,
    }


def get_category_faqs(category_slug: str | None = None) -> list[dict]:
    """Return FAQ list for category or all-tools page."""
    key = category_slug or "all"
    return CATEGORY_FAQS.get(key, CATEGORY_FAQS["all"])


def get_related_tools(slug: str, db: Session | None = None, limit: int = 4) -> list[dict]:
    """Return related tools from config or same category."""
    config = get_tool_config(slug)
    if config and config.get("related_slugs"):
        tools = []
        for s in config["related_slugs"][:limit]:
            t = get_tool_by_slug(s, db)
            if t:
                tools.append(t)
        if tools:
            return tools
    tool = get_tool_by_slug(slug, db)
    if not tool:
        return get_popular_tools(limit)
    same_cat = [t for t in get_tools_by_category(tool.get("category"), db) if t["slug"] != slug]
    return same_cat[:limit] or get_popular_tools(limit)


def get_tool_page_config(slug: str) -> dict:
    """Return full tool page config."""
    config = get_tool_config(slug)
    if config:
        return config
    tool = get_tool_by_slug(slug)
    if tool:
        return get_default_config(tool)
    return get_default_config({"name": slug, "description": ""})


def get_popular_tools_list(db: Session | None = None, limit: int = 6) -> list[dict]:
    tools = [t for t in get_all_tools(db) if t.get("is_popular")]
    return sorted(tools, key=lambda t: t.get("sort_order", 99))[:limit]


def get_latest_tools_list(db: Session | None = None, limit: int = 4) -> list[dict]:
    return sorted(get_all_tools(db), key=lambda t: t.get("sort_order", 99), reverse=True)[:limit]
