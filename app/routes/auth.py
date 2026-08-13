"""User auth routes — register, login, logout, account."""

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.auth_service import (
    authenticate_user,
    login_user,
    logout_user,
    register_user,
)
from app.services.usage_service import check_ai_limit
from app.utils.page_context import page_context
from app.utils.templates import templates

router = APIRouter(tags=["auth"])


@router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request, db: Session = Depends(get_db)) -> HTMLResponse:
    ctx = page_context(request, db)
    if ctx["is_logged_in"]:
        return RedirectResponse("/account", status_code=302)
    return templates.TemplateResponse(
        request=request,
        name="auth/register.html",
        context={**ctx, "error": None, "page_title": f"Create Account | {ctx['app_name']}"},
    )


@router.post("/register")
async def register_submit(
    request: Request,
    email: str = Form(),
    password: str = Form(),
    db: Session = Depends(get_db),
):
    user, err = register_user(db, email, password)
    if err:
        ctx = page_context(request, db, error=err, page_title="Create Account")
        return templates.TemplateResponse(
            request=request, name="auth/register.html", context=ctx, status_code=400
        )
    login_user(request, user)
    return RedirectResponse("/account", status_code=302)


@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request, db: Session = Depends(get_db)) -> HTMLResponse:
    ctx = page_context(request, db)
    if ctx["is_logged_in"]:
        return RedirectResponse("/account", status_code=302)
    return templates.TemplateResponse(
        request=request,
        name="auth/login.html",
        context={**ctx, "error": None, "page_title": f"Sign In | {ctx['app_name']}"},
    )


@router.post("/login")
async def login_submit(
    request: Request,
    email: str = Form(),
    password: str = Form(),
    db: Session = Depends(get_db),
):
    user = authenticate_user(db, email, password)
    if not user:
        ctx = page_context(request, db, error="Invalid email or password.", page_title="Sign In")
        return templates.TemplateResponse(
            request=request, name="auth/login.html", context=ctx, status_code=401
        )
    login_user(request, user)
    next_url = request.query_params.get("next", "/account")
    return RedirectResponse(next_url, status_code=302)


@router.get("/logout")
async def logout(request: Request):
    logout_user(request)
    return RedirectResponse("/", status_code=302)


@router.get("/account", response_class=HTMLResponse)
async def account_page(request: Request, db: Session = Depends(get_db)) -> HTMLResponse:
    ctx = page_context(request, db)
    if not ctx["is_logged_in"]:
        return RedirectResponse("/login?next=/account", status_code=302)
    usage = check_ai_limit(request)
    return templates.TemplateResponse(
        request=request,
        name="auth/account.html",
        context={
            **ctx,
            "usage": usage,
            "page_title": f"My Account | {ctx['app_name']}",
            "page_description": "Manage your Seller Toolkit account and AI usage.",
            "canonical_url": ctx["site_url"] + "/account",
        },
    )
