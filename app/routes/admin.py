"""Admin panel routes — Sprint 5, Chinese UI."""

from fastapi import APIRouter, Depends, Form, HTTPException, Query, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session

from app.config import get_settings
from app.database import get_db
from app.services.admin_content_service import (
    create_blog_post,
    create_tool,
    delete_blog_post,
    delete_tool,
    get_blog_admin,
    get_tool_admin,
    list_blog_admin,
    list_categories_admin,
    list_tools_admin,
    update_blog_post,
    update_tool,
)
from app.services.admin_ops_service import list_leads, list_payments
from app.services.admin_user_service import (
    get_user,
    list_subscriptions,
    list_users,
    set_user_tier_admin,
    toggle_user_active,
)
from app.services.stats_service import get_dashboard_stats
from app.services.settings_service import EDITABLE_KEYS, get_all_settings, save_settings_batch
from app.payment import get_payment_provider
from app.data.seed_blog import SEED_BLOG_POSTS
from app.data.seed_tools import SEED_TOOLS
from app.data.tool_categories import TOOL_CATEGORIES
from app.utils.templates import templates

router = APIRouter(prefix="/admin", tags=["admin"])
settings = get_settings()


def _is_logged_in(request: Request) -> bool:
    return request.session.get("admin_logged_in") is True


def _require_login(request: Request):
    if not _is_logged_in(request):
        raise HTTPException(status_code=303, headers={"Location": "/admin/login"})


@router.get("/login", response_class=HTMLResponse)
async def admin_login_page(request: Request) -> HTMLResponse:
    if _is_logged_in(request):
        return RedirectResponse("/admin/", status_code=302)
    return templates.TemplateResponse(request=request, name="admin/login.html", context={
        "app_name": settings.app_name, "error": None,
    })


@router.post("/login")
async def admin_login(request: Request, username: str = Form(), password: str = Form()):
    if username == settings.admin_username and password == settings.admin_password:
        request.session["admin_logged_in"] = True
        request.session["admin_user"] = username
        return RedirectResponse("/admin/", status_code=302)
    return templates.TemplateResponse(request=request, name="admin/login.html", context={
        "app_name": settings.app_name, "error": "用户名或密码错误",
    }, status_code=401)


@router.get("/logout")
async def admin_logout(request: Request):
    request.session.clear()
    return RedirectResponse("/admin/login", status_code=302)


@router.get("/", response_class=HTMLResponse)
async def admin_dashboard(request: Request) -> HTMLResponse:
    if not _is_logged_in(request):
        return RedirectResponse("/admin/login", status_code=302)
    return templates.TemplateResponse(request=request, name="admin/dashboard.html", context={
        "app_name": settings.app_name,
        "admin_user": request.session.get("admin_user", "admin"),
        "tool_count": len(SEED_TOOLS),
        "blog_count": len(SEED_BLOG_POSTS),
        "category_count": len(TOOL_CATEGORIES),
        "stats": get_dashboard_stats(),
        "debug": settings.debug,
        "payment_provider": settings.payment_provider,
        "payments_live": get_payment_provider().is_available(),
    })


@router.get("/tools", response_class=HTMLResponse)
async def admin_tools(request: Request, db: Session = Depends(get_db)) -> HTMLResponse:
    if not _is_logged_in(request):
        return RedirectResponse("/admin/login", status_code=302)
    tools = list_tools_admin(db) or SEED_TOOLS
    cats = list_categories_admin(db)
    return templates.TemplateResponse(request=request, name="admin/tools.html", context={
        "app_name": settings.app_name,
        "admin_user": request.session.get("admin_user"),
        "tools": tools,
        "categories": {c.slug: c for c in cats} if cats else TOOL_CATEGORIES,
    })


@router.get("/tools/new", response_class=HTMLResponse)
async def admin_tool_new(request: Request, db: Session = Depends(get_db)) -> HTMLResponse:
    if not _is_logged_in(request):
        return RedirectResponse("/admin/login", status_code=302)
    return templates.TemplateResponse(request=request, name="admin/tool_form.html", context={
        "app_name": settings.app_name,
        "admin_user": request.session.get("admin_user"),
        "tool": None,
        "categories": list_categories_admin(db),
        "error": None,
    })


@router.get("/tools/{tool_id}/edit", response_class=HTMLResponse)
async def admin_tool_edit(request: Request, tool_id: int, db: Session = Depends(get_db)) -> HTMLResponse:
    if not _is_logged_in(request):
        return RedirectResponse("/admin/login", status_code=302)
    tool = get_tool_admin(db, tool_id)
    if not tool:
        raise HTTPException(status_code=404, detail="Tool not found")
    return templates.TemplateResponse(request=request, name="admin/tool_form.html", context={
        "app_name": settings.app_name,
        "admin_user": request.session.get("admin_user"),
        "tool": tool,
        "categories": list_categories_admin(db),
        "error": None,
    })


@router.post("/tools/save")
async def admin_tool_save(
    request: Request,
    db: Session = Depends(get_db),
    tool_id: int | None = Form(None),
    name: str = Form(),
    slug: str = Form(),
    category_id: int = Form(),
    description: str = Form(""),
    intro: str = Form(""),
    icon: str = Form("wrench"),
    is_ai: str | None = Form(None),
    is_popular: str | None = Form(None),
    is_featured: str | None = Form(None),
    sort_order: int = Form(99),
    status: str | None = Form(None),
):
    if not _is_logged_in(request):
        return RedirectResponse("/admin/login", status_code=302)
    data = {
        "name": name.strip(), "slug": slug.strip(), "category_id": category_id,
        "description": description, "intro": intro or description, "icon": icon,
        "is_ai": is_ai == "true",
        "is_popular": is_popular == "true",
        "is_featured": is_featured == "true",
        "sort_order": sort_order,
        "status": status == "true",
    }
    if tool_id:
        tool = get_tool_admin(db, tool_id)
        if tool:
            update_tool(db, tool, data)
    else:
        create_tool(db, data)
    return RedirectResponse("/admin/tools", status_code=302)


@router.post("/tools/{tool_id}/delete")
async def admin_tool_delete(request: Request, tool_id: int, db: Session = Depends(get_db)):
    if not _is_logged_in(request):
        return RedirectResponse("/admin/login", status_code=302)
    tool = get_tool_admin(db, tool_id)
    if tool:
        delete_tool(db, tool)
    return RedirectResponse("/admin/tools", status_code=302)


@router.get("/blog", response_class=HTMLResponse)
async def admin_blog(request: Request, db: Session = Depends(get_db)) -> HTMLResponse:
    if not _is_logged_in(request):
        return RedirectResponse("/admin/login", status_code=302)
    posts = list_blog_admin(db) or [
        {"id": None, "title": p["title"], "slug": p["slug"], "category": p.get("category", ""),
         "published_date": p.get("published_date", ""), "status": "seed"}
        for p in SEED_BLOG_POSTS
    ]
    return templates.TemplateResponse(request=request, name="admin/blog.html", context={
        "app_name": settings.app_name,
        "admin_user": request.session.get("admin_user"),
        "posts": posts,
    })


@router.get("/blog/new", response_class=HTMLResponse)
async def admin_blog_new(request: Request) -> HTMLResponse:
    if not _is_logged_in(request):
        return RedirectResponse("/admin/login", status_code=302)
    return templates.TemplateResponse(request=request, name="admin/blog_form.html", context={
        "app_name": settings.app_name, "admin_user": request.session.get("admin_user"),
        "post": None, "error": None,
    })


@router.get("/blog/{post_id}/edit", response_class=HTMLResponse)
async def admin_blog_edit(request: Request, post_id: int, db: Session = Depends(get_db)) -> HTMLResponse:
    if not _is_logged_in(request):
        return RedirectResponse("/admin/login", status_code=302)
    post = get_blog_admin(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return templates.TemplateResponse(request=request, name="admin/blog_form.html", context={
        "app_name": settings.app_name, "admin_user": request.session.get("admin_user"),
        "post": post, "error": None,
    })


@router.post("/blog/save")
async def admin_blog_save(
    request: Request,
    db: Session = Depends(get_db),
    post_id: int | None = Form(None),
    title: str = Form(),
    slug: str = Form(),
    summary: str = Form(""),
    content: str = Form(""),
    category: str = Form(""),
    tags: str = Form(""),
    seo_title: str = Form(""),
    seo_description: str = Form(""),
    publish: str | None = Form(None),
):
    if not _is_logged_in(request):
        return RedirectResponse("/admin/login", status_code=302)
    data = {
        "title": title.strip(), "slug": slug.strip(), "summary": summary, "content": content,
        "category": category, "tags": tags, "seo_title": seo_title, "seo_description": seo_description,
        "publish": publish == "true",
    }
    if post_id:
        post = get_blog_admin(db, post_id)
        if post:
            update_blog_post(db, post, data)
    else:
        create_blog_post(db, data)
    return RedirectResponse("/admin/blog", status_code=302)


@router.post("/blog/{post_id}/delete")
async def admin_blog_delete(request: Request, post_id: int, db: Session = Depends(get_db)):
    if not _is_logged_in(request):
        return RedirectResponse("/admin/login", status_code=302)
    post = get_blog_admin(db, post_id)
    if post:
        delete_blog_post(db, post)
    return RedirectResponse("/admin/blog", status_code=302)


@router.get("/users", response_class=HTMLResponse)
async def admin_users(request: Request, db: Session = Depends(get_db)) -> HTMLResponse:
    if not _is_logged_in(request):
        return RedirectResponse("/admin/login", status_code=302)
    return templates.TemplateResponse(request=request, name="admin/users.html", context={
        "app_name": settings.app_name,
        "admin_user": request.session.get("admin_user"),
        "users": list_users(db),
    })


@router.get("/users/{user_id}/edit", response_class=HTMLResponse)
async def admin_user_edit(request: Request, user_id: int, db: Session = Depends(get_db)) -> HTMLResponse:
    if not _is_logged_in(request):
        return RedirectResponse("/admin/login", status_code=302)
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return templates.TemplateResponse(request=request, name="admin/user_edit.html", context={
        "app_name": settings.app_name,
        "admin_user": request.session.get("admin_user"),
        "user": user,
        "saved": False,
    })


@router.post("/users/{user_id}/save")
async def admin_user_save(
    request: Request,
    user_id: int,
    db: Session = Depends(get_db),
    tier: str = Form("registered"),
    is_active: str | None = Form(None),
):
    if not _is_logged_in(request):
        return RedirectResponse("/admin/login", status_code=302)
    user = get_user(db, user_id)
    if user:
        set_user_tier_admin(db, user, tier)
        toggle_user_active(db, user, is_active == "true")
    return RedirectResponse(f"/admin/users/{user_id}/edit?saved=1", status_code=302)


@router.get("/leads", response_class=HTMLResponse)
async def admin_leads(request: Request, db: Session = Depends(get_db)) -> HTMLResponse:
    if not _is_logged_in(request):
        return RedirectResponse("/admin/login", status_code=302)
    return templates.TemplateResponse(request=request, name="admin/leads.html", context={
        "app_name": settings.app_name,
        "admin_user": request.session.get("admin_user"),
        "leads": list_leads(db),
    })


@router.get("/payments", response_class=HTMLResponse)
async def admin_payments(request: Request, db: Session = Depends(get_db)) -> HTMLResponse:
    if not _is_logged_in(request):
        return RedirectResponse("/admin/login", status_code=302)
    return templates.TemplateResponse(request=request, name="admin/payments.html", context={
        "app_name": settings.app_name,
        "admin_user": request.session.get("admin_user"),
        "payments": list_payments(db),
        "subscriptions": list_subscriptions(db),
        "payment_provider": settings.payment_provider,
        "payments_live": get_payment_provider().is_available(),
    })


@router.get("/settings", response_class=HTMLResponse)
async def admin_settings(request: Request, db: Session = Depends(get_db)) -> HTMLResponse:
    if not _is_logged_in(request):
        return RedirectResponse("/admin/login", status_code=302)
    db_settings = get_all_settings(db)
    return templates.TemplateResponse(request=request, name="admin/settings.html", context={
        "app_name": settings.app_name,
        "admin_user": request.session.get("admin_user"),
        "domain": settings.domain,
        "has_ai_key": bool(settings.deepseek_api_key),
        "debug": settings.debug,
        "payment_provider": settings.payment_provider,
        "payments_live": get_payment_provider().is_available(),
        "env_ga": settings.ga_measurement_id,
        "db_settings": db_settings,
        "editable_keys": EDITABLE_KEYS,
        "saved": request.query_params.get("saved") == "1",
    })


@router.post("/settings/save")
async def admin_settings_save(request: Request, db: Session = Depends(get_db)):
    if not _is_logged_in(request):
        return RedirectResponse("/admin/login", status_code=302)
    form = await request.form()
    data = {key: form.get(key, "") for key in EDITABLE_KEYS}
    save_settings_batch(db, data)
    return RedirectResponse("/admin/settings?saved=1", status_code=302)
