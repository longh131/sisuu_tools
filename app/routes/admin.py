"""Admin panel routes — Sprint 5, Chinese UI."""

from fastapi import APIRouter, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse

from app.config import get_settings
from app.services.stats_service import get_dashboard_stats
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
    })


@router.get("/tools", response_class=HTMLResponse)
async def admin_tools(request: Request) -> HTMLResponse:
    if not _is_logged_in(request):
        return RedirectResponse("/admin/login", status_code=302)
    return templates.TemplateResponse(request=request, name="admin/tools.html", context={
        "app_name": settings.app_name,
        "admin_user": request.session.get("admin_user"),
        "tools": SEED_TOOLS,
        "categories": TOOL_CATEGORIES,
    })


@router.get("/blog", response_class=HTMLResponse)
async def admin_blog(request: Request) -> HTMLResponse:
    if not _is_logged_in(request):
        return RedirectResponse("/admin/login", status_code=302)
    return templates.TemplateResponse(request=request, name="admin/blog.html", context={
        "app_name": settings.app_name,
        "admin_user": request.session.get("admin_user"),
        "posts": SEED_BLOG_POSTS,
    })


@router.get("/settings", response_class=HTMLResponse)
async def admin_settings(request: Request) -> HTMLResponse:
    if not _is_logged_in(request):
        return RedirectResponse("/admin/login", status_code=302)
    return templates.TemplateResponse(request=request, name="admin/settings.html", context={
        "app_name": settings.app_name,
        "admin_user": request.session.get("admin_user"),
        "domain": settings.domain,
        "has_ai_key": bool(settings.deepseek_api_key),
        "debug": settings.debug,
    })
