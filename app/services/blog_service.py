"""Blog service — DB-first with seed fallback."""

from sqlalchemy.orm import Session

from app.data.seed_blog import SEED_BLOG_POSTS


def _post_from_db(row) -> dict:
    return {
        "title": row.title,
        "slug": row.slug,
        "summary": row.summary or "",
        "content": row.content or "",
        "category": row.category or "",
        "tags": row.tags or "",
        "seo_title": row.seo_title or "",
        "seo_description": row.seo_description or "",
        "published_date": row.published_at.strftime("%Y-%m-%d") if row.published_at else "",
    }


def _load_posts(db: Session | None = None) -> list[dict]:
    if db:
        try:
            from app.models.blog_post import BlogPost
            rows = (
                db.query(BlogPost)
                .filter(BlogPost.published_at.isnot(None))
                .order_by(BlogPost.published_at.desc())
                .all()
            )
            if rows:
                return [_post_from_db(r) for r in rows]
        except Exception:
            pass
    return list(SEED_BLOG_POSTS)


def get_all_posts(db: Session | None = None) -> list[dict]:
    return _load_posts(db)


def get_post_by_slug(slug: str, db: Session | None = None) -> dict | None:
    for post in _load_posts(db):
        if post["slug"] == slug:
            return post
    return None


def get_related_posts(slug: str, db: Session | None = None, limit: int = 4) -> list[dict]:
    """Return related blog posts by shared category or tags."""
    posts = _load_posts(db)
    current = next((p for p in posts if p["slug"] == slug), None)
    if not current:
        return posts[:limit]

    current_tags = set((current.get("tags") or "").split(","))
    scored: list[tuple[int, dict]] = []

    for post in posts:
        if post["slug"] == slug:
            continue
        score = 0
        if post.get("category") == current.get("category"):
            score += 2
        post_tags = set((post.get("tags") or "").split(","))
        score += len(current_tags & post_tags)
        if score > 0:
            scored.append((score, post))

    scored.sort(key=lambda x: x[0], reverse=True)
    related = [p for _, p in scored[:limit]]

    if len(related) < limit:
        for post in posts:
            if post["slug"] != slug and post not in related:
                related.append(post)
            if len(related) >= limit:
                break

    return related[:limit]
