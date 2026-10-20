"""SEO routes — robots.txt, sitemap.xml, and site verification files."""

from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse, PlainTextResponse, Response
from sqlalchemy.orm import Session

from app.database import get_db
from app.utils.seo import generate_robots_txt, generate_sitemap_xml

router = APIRouter(tags=["seo"])

VERIFY_DIR = Path(__file__).resolve().parent.parent / "verify"


@router.get("/robots.txt", response_class=PlainTextResponse)
async def robots_txt() -> str:
    """Serve robots.txt for search engine crawlers."""
    return generate_robots_txt()


@router.get("/sitemap.xml")
async def sitemap_xml(db: Session = Depends(get_db)) -> Response:
    """Serve dynamically generated sitemap.xml."""
    content = generate_sitemap_xml(db)
    return Response(content=content, media_type="application/xml")


@router.get("/BingSiteAuth.xml")
async def bing_site_auth() -> FileResponse:
    """Bing Webmaster XML verification — file must live in app/verify/."""
    path = VERIFY_DIR / "BingSiteAuth.xml"
    if not path.is_file():
        raise HTTPException(status_code=404, detail="BingSiteAuth.xml not found")
    return FileResponse(path, media_type="application/xml")
