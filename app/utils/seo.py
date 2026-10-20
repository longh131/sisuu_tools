"""SEO schema helpers."""

import json


def faq_schema(faqs: list[dict]) -> str:
    """Return FAQPage JSON-LD string."""
    if not faqs:
        return ""
    entities = [
        {
            "@type": "Question",
            "name": item["question"],
            "acceptedAnswer": {"@type": "Answer", "text": item["answer"]},
        }
        for item in faqs
    ]
    return json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": entities})


def breadcrumb_schema(breadcrumbs: list[dict], site_url: str) -> str:
    """Return BreadcrumbList JSON-LD string."""
    items = []
    for i, crumb in enumerate(breadcrumbs):
        if crumb.get("url"):
            items.append({
                "@type": "ListItem",
                "position": i + 1,
                "name": crumb["name"],
                "item": site_url + crumb["url"],
            })
        else:
            items.append({
                "@type": "ListItem",
                "position": i + 1,
                "name": crumb["name"],
            })
    return json.dumps({
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": items,
    })


def software_app_schema(tool: dict, site_url: str) -> str:
    """Return SoftwareApplication JSON-LD for tool pages."""
    return json.dumps({
        "@context": "https://schema.org",
        "@type": "SoftwareApplication",
        "name": tool["name"],
        "description": tool.get("description", ""),
        "url": f"{site_url}/tools/{tool['slug']}",
        "applicationCategory": "BusinessApplication",
        "operatingSystem": "Web",
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
    })


def article_schema(post: dict, site_url: str) -> str:
    """Return Article JSON-LD for blog posts."""
    schema = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": post["title"],
        "description": post.get("summary", ""),
        "url": f"{site_url}/blog/{post['slug']}",
        "author": {"@type": "Organization", "name": "Seller Toolkit"},
        "publisher": {
            "@type": "Organization",
            "name": "Seller Toolkit",
            "logo": {"@type": "ImageObject", "url": f"{site_url}/static/icons/favicon.svg"},
        },
        "image": f"{site_url}/static/images/og-default.png",
        "mainEntityOfPage": f"{site_url}/blog/{post['slug']}",
    }
    if post.get("published_date"):
        schema["datePublished"] = post["published_date"]
    return json.dumps(schema)


# ── Sitemap & robots ──

from datetime import datetime, timezone

from app.config import get_settings
from app.data.seed_blog import SEED_BLOG_POSTS
from app.data.seed_tools import SEED_TOOLS
from app.data.tool_categories import CATEGORY_TAB_ORDER, TOOL_CATEGORIES

settings = get_settings()

STATIC_PAGES: list[dict] = [
    {"loc": "/", "priority": "1.0", "changefreq": "weekly"},
    {"loc": "/tools", "priority": "0.9", "changefreq": "weekly"},
    {"loc": "/about", "priority": "0.6", "changefreq": "monthly"},
    {"loc": "/contact", "priority": "0.6", "changefreq": "monthly"},
    {"loc": "/privacy", "priority": "0.4", "changefreq": "yearly"},
    {"loc": "/terms", "priority": "0.4", "changefreq": "yearly"},
    {"loc": "/pricing", "priority": "0.5", "changefreq": "monthly"},
    {"loc": "/blog", "priority": "0.7", "changefreq": "weekly"},
]


def _today() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def generate_robots_txt() -> str:
    return f"""User-agent: *
Allow: /

Disallow: /admin/
Disallow: /api/

Sitemap: {settings.site_url}/sitemap.xml
"""


def generate_sitemap_xml(db=None) -> str:
    urls: list[str] = []
    for page in STATIC_PAGES:
        urls.append(_sitemap_entry(page["loc"], page["priority"], page["changefreq"]))
    for slug in CATEGORY_TAB_ORDER:
        urls.append(_sitemap_entry(f"/tools/{slug}", "0.8", "weekly"))
    for tool in SEED_TOOLS:
        urls.append(_sitemap_entry(f"/tools/{tool['slug']}", "0.8", "monthly"))
    blog_slugs: list[str] = []
    if db is not None:
        try:
            from app.services.blog_service import get_all_posts

            blog_slugs = [p["slug"] for p in get_all_posts(db)]
        except Exception:
            blog_slugs = []
    if not blog_slugs:
        blog_slugs = [p["slug"] for p in SEED_BLOG_POSTS]
    else:
        from app.data.synced_blog_posts import SYNCED_BLOG_POSTS

        seen = set(blog_slugs)
        for p in SYNCED_BLOG_POSTS:
            if p["slug"] not in seen:
                blog_slugs.append(p["slug"])
                seen.add(p["slug"])
    for slug in blog_slugs:
        urls.append(_sitemap_entry(f"/blog/{slug}", "0.7", "monthly"))
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(urls) + "\n</urlset>\n"
    )


def _sitemap_entry(path: str, priority: str, changefreq: str) -> str:
    loc = settings.site_url + path
    return (
        f"  <url>\n    <loc>{loc}</loc>\n"
        f"    <lastmod>{_today()}</lastmod>\n"
        f"    <changefreq>{changefreq}</changefreq>\n"
        f"    <priority>{priority}</priority>\n  </url>"
    )
