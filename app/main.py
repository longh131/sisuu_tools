"""
FastAPI application entry point.
"""

from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from app.config import get_settings
from app.routes.admin import router as admin_router
from app.routes.api import router as api_router
from app.routes.blog import router as blog_router
from app.routes.home import router as home_router
from app.routes.leads import router as leads_router
from app.routes.pages import router as pages_router
from app.routes.seo import router as seo_router
from app.routes.tools import router as tools_router
from app.utils.logger import get_logger, setup_logging
from app.utils.static_assets import STATIC_VERSION
from app.utils.templates import templates

settings = get_settings()
logger = get_logger("main")


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    logger.info("Starting %s (debug=%s)", settings.app_name, settings.debug)
    yield
    logger.info("Shutting down %s", settings.app_name)


app = FastAPI(title=settings.app_name, debug=settings.debug, lifespan=lifespan)

# Session middleware for admin auth
app.add_middleware(SessionMiddleware, secret_key=settings.secret_key)


@app.middleware("http")
async def cache_and_security_headers(request: Request, call_next):
    """Add cache headers for static assets and basic security headers."""
    response = await call_next(request)
    path = request.url.path
    if path.startswith("/static/"):
        response.headers["Cache-Control"] = "public, max-age=31536000, immutable"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    return response


# Static assets
static_dir = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

# Routes (order matters — specific routes before catch-all)
app.include_router(home_router)
app.include_router(tools_router)
app.include_router(blog_router)
app.include_router(pages_router)
app.include_router(leads_router)
app.include_router(api_router)
app.include_router(admin_router)
app.include_router(seo_router)


@app.get("/health")
async def health_check() -> dict:
    return {"status": "ok", "app": settings.app_name}


@app.exception_handler(404)
async def not_found_handler(request: Request, exc) -> HTMLResponse:
    """Custom 404 page for browser requests."""
    if request.url.path.startswith("/api/"):
        from fastapi.responses import JSONResponse
        return JSONResponse({"detail": "Not found"}, status_code=404)
    ctx = {
        "app_name": settings.app_name,
        "site_url": settings.site_url,
        "page_title": f"404 — Page Not Found | {settings.app_name}",
        "page_description": "The page you are looking for does not exist.",
        "canonical_url": settings.site_url + request.url.path,
        "static_version": STATIC_VERSION,
        "og_image_url": f"{settings.site_url}/static/images/og-default.png",
        "cdn": {},
    }
    return templates.TemplateResponse(request=request, name="404.html", context=ctx, status_code=404)
