#!/usr/bin/env python3
"""Upsert marketing blog posts from app/data/synced_blog_posts.py into MySQL.

Safe to run on every deploy — updates existing slugs, inserts new ones.
Usage: python scripts/sync_blog_posts.py
"""

import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from app.data.synced_blog_posts import SYNCED_BLOG_POSTS
from app.database import SessionLocal
from app.models.blog_post import BlogPost


def parse_date(value: str | None) -> datetime:
    if not value:
        return datetime.utcnow()
    try:
        return datetime.strptime(value[:10], "%Y-%m-%d")
    except ValueError:
        return datetime.utcnow()


def sync_posts(db) -> tuple[int, int]:
    inserted = 0
    updated = 0
    for p in SYNCED_BLOG_POSTS:
        slug = p["slug"]
        row = db.query(BlogPost).filter(BlogPost.slug == slug).first()
        fields = {
            "title": p["title"],
            "summary": p.get("summary", ""),
            "content": p.get("content", ""),
            "category": p.get("category", ""),
            "tags": p.get("tags", ""),
            "seo_title": p.get("seo_title", ""),
            "seo_description": p.get("seo_description", ""),
            "published_at": parse_date(p.get("published_date")),
        }
        if row:
            for key, val in fields.items():
                setattr(row, key, val)
            updated += 1
        else:
            db.add(BlogPost(slug=slug, **fields))
            inserted += 1
    db.commit()
    return inserted, updated


def main() -> int:
    print("=== Sync blog posts ===")
    db = SessionLocal()
    try:
        inserted, updated = sync_posts(db)
        print(f"[OK] inserted={inserted} updated={updated} total_defs={len(SYNCED_BLOG_POSTS)}")
    except Exception as exc:
        print(f"[FAIL] {exc}")
        return 1
    finally:
        db.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
