"""Blog routes — Sprint 6 + V1.1 DB support."""

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.blog_service import get_all_posts, get_post_by_slug, get_related_posts
from app.utils.seo import article_schema, breadcrumb_schema
from app.utils.templates import base_context, templates

router = APIRouter(tags=["blog"])


@router.get("/blog", response_class=HTMLResponse, name="blog")
async def blog_list(request: Request, db: Session = Depends(get_db)) -> HTMLResponse:
    ctx = base_context()
    crumbs = [{"name": "Home", "url": "/"}, {"name": "Blog", "url": ""}]
    return templates.TemplateResponse(
        request=request,
        name="blog.html",
        context={
            **ctx,
            "page_title": f"Seller Blog — Guides & Tips | {ctx['app_name']}",
            "page_description": "Expert seller guides, Amazon tips and eCommerce tutorials for global sellers.",
            "canonical_url": ctx["site_url"] + "/blog",
            "posts": get_all_posts(db),
            "breadcrumbs": crumbs,
            "schema_breadcrumb": breadcrumb_schema(crumbs, ctx["site_url"]),
        },
    )


@router.get("/blog/{slug}", response_class=HTMLResponse, name="blog_post")
async def blog_detail(request: Request, slug: str, db: Session = Depends(get_db)) -> HTMLResponse:
    post = get_post_by_slug(slug, db)
    if not post:
        raise HTTPException(status_code=404, detail="Article not found")

    ctx = base_context()
    crumbs = [
        {"name": "Home", "url": "/"},
        {"name": "Blog", "url": "/blog"},
        {"name": post["title"], "url": ""},
    ]
    return templates.TemplateResponse(
        request=request,
        name="blog_post.html",
        context={
            **ctx,
            "page_title": post.get("seo_title") or f"{post['title']} — {ctx['app_name']}",
            "page_description": post.get("seo_description") or post.get("summary", ""),
            "canonical_url": ctx["site_url"] + f"/blog/{slug}",
            "post": post,
            "related_posts": get_related_posts(slug, db),
            "breadcrumbs": crumbs,
            "schema_article": article_schema(post, ctx["site_url"]),
            "schema_breadcrumb": breadcrumb_schema(crumbs, ctx["site_url"]),
        },
    )
