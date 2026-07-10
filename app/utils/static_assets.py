"""
Static asset URL helpers.
Centralises versioned paths for cache busting and local vendor assets.
"""

from app.config import get_settings

settings = get_settings()

# Bump on each release to invalidate browser cache
STATIC_VERSION = "1.0.1"

# Self-hosted vendor assets (Sprint 8 — no external CDN for core resources)
CDN_ASSETS: dict[str, str] = {
    "bootstrap_css": "/static/vendor/bootstrap.min.css",
    "bootstrap_js": "/static/vendor/bootstrap.bundle.min.js",
    "lucide_js": "/static/vendor/lucide.min.js",
}


def static_url(path: str) -> str:
    """Return a versioned static asset URL for cache busting."""
    clean = path.lstrip("/")
    return f"/static/{clean}?v={STATIC_VERSION}"


def vendor_url(path: str) -> str:
    """Return a versioned vendor asset URL."""
    clean = path.lstrip("/")
    return f"/static/vendor/{clean}?v={STATIC_VERSION}"


def og_image_url() -> str:
    """Return the default Open Graph image absolute URL."""
    return f"{settings.site_url}/static/images/og-default.png"
