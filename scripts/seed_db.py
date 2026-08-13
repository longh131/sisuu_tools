#!/usr/bin/env python3
"""Seed MySQL from Python seed files — run once after migration.

Usage: python scripts/seed_db.py
"""

import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from app.data.seed_blog import SEED_BLOG_POSTS
from app.data.seed_tools import SEED_TOOLS
from app.data.tool_categories import CATEGORY_TAB_ORDER, TOOL_CATEGORIES
from app.database import SessionLocal
from app.models.blog_post import BlogPost
from app.models.tool import Tool
from app.models.tool_category import ToolCategory


def parse_date(value: str | None):
    if not value:
        return datetime.utcnow()
    try:
        return datetime.strptime(value[:10], "%Y-%m-%d")
    except ValueError:
        return datetime.utcnow()


def seed_categories(db) -> dict[str, int]:
    slug_to_id: dict[str, int] = {}
    for i, slug in enumerate(CATEGORY_TAB_ORDER):
        cat = TOOL_CATEGORIES.get(slug)
        if not cat:
            continue
        row = db.query(ToolCategory).filter(ToolCategory.slug == slug).first()
        if not row:
            row = ToolCategory(
                name=cat["name"],
                slug=slug,
                icon=cat.get("icon", "folder"),
                description=cat.get("description", ""),
                sort_order=i + 1,
                status=True,
            )
            db.add(row)
            db.flush()
        slug_to_id[slug] = row.id
    db.commit()
    return slug_to_id


def seed_tools(db, slug_to_id: dict[str, int]) -> int:
    if db.query(Tool).count() > 0:
        print("[SKIP] tools already seeded")
        return 0
    count = 0
    for t in SEED_TOOLS:
        cat_slug = t.get("category", "calculators")
        cat_id = slug_to_id.get(cat_slug)
        if not cat_id:
            continue
        db.add(Tool(
            category_id=cat_id,
            name=t["name"],
            slug=t["slug"],
            description=t.get("description", ""),
            intro=t.get("intro", t.get("description", "")),
            icon=t.get("icon", "wrench"),
            is_ai=t.get("is_ai", False),
            is_popular=t.get("is_popular", False),
            is_featured=t.get("is_featured", False),
            sort_order=t.get("sort_order", 99),
            status=True,
        ))
        count += 1
    db.commit()
    return count


def seed_blog(db) -> int:
    if db.query(BlogPost).count() > 0:
        print("[SKIP] blog already seeded")
        return 0
    count = 0
    for p in SEED_BLOG_POSTS:
        db.add(BlogPost(
            title=p["title"],
            slug=p["slug"],
            summary=p.get("summary", ""),
            content=p.get("content", ""),
            category=p.get("category", ""),
            tags=p.get("tags", ""),
            seo_title=p.get("seo_title", ""),
            seo_description=p.get("seo_description", ""),
            published_at=parse_date(p.get("published_date")),
        ))
        count += 1
    db.commit()
    return count


def main() -> int:
    print("=== Seed DB ===")
    db = SessionLocal()
    try:
        cats = seed_categories(db)
        print(f"[OK] categories: {len(cats)}")
        n_tools = seed_tools(db, cats)
        print(f"[OK] tools inserted: {n_tools}")
        n_blog = seed_blog(db)
        print(f"[OK] blog inserted: {n_blog}")
    finally:
        db.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
