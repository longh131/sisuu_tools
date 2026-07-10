"""SEO routes — robots.txt and sitemap.xml."""

from fastapi import APIRouter
from fastapi.responses import PlainTextResponse, Response

from app.utils.seo import generate_robots_txt, generate_sitemap_xml

router = APIRouter(tags=["seo"])


@router.get("/robots.txt", response_class=PlainTextResponse)
async def robots_txt() -> str:
    """Serve robots.txt for search engine crawlers."""
    return generate_robots_txt()


@router.get("/sitemap.xml")
async def sitemap_xml() -> Response:
    """Serve dynamically generated sitemap.xml."""
    content = generate_sitemap_xml()
    return Response(content=content, media_type="application/xml")
