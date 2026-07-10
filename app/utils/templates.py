"""
Shared Jinja2 template engine with global context variables.
"""

from fastapi.templating import Jinja2Templates

from app.config import get_settings
from app.utils.seo import article_schema, breadcrumb_schema, faq_schema, software_app_schema
from app.utils.static_assets import CDN_ASSETS, STATIC_VERSION, og_image_url, static_url, vendor_url

settings = get_settings()

templates = Jinja2Templates(directory="app/templates")

templates.env.globals["static_version"] = STATIC_VERSION
templates.env.globals["static_url"] = static_url
templates.env.globals["vendor_url"] = vendor_url
templates.env.globals["og_image_url"] = og_image_url()
templates.env.globals["cdn"] = CDN_ASSETS
templates.env.globals["faq_schema"] = faq_schema
templates.env.globals["breadcrumb_schema"] = breadcrumb_schema
templates.env.globals["software_app_schema"] = software_app_schema
templates.env.globals["article_schema"] = article_schema


def base_context() -> dict:
    """Return common template context shared across all pages."""
    return {
        "app_name": settings.app_name,
        "site_url": settings.site_url,
        "static_version": STATIC_VERSION,
        "og_image_url": og_image_url(),
        "cdn": CDN_ASSETS,
        "ga_measurement_id": settings.ga_measurement_id,
    }
