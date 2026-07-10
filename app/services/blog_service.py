"""Blog service — related posts and helpers."""

from app.data.seed_blog import SEED_BLOG_POSTS


def get_related_posts(slug: str, limit: int = 4) -> list[dict]:
    """Return related blog posts by shared category or tags."""
    current = next((p for p in SEED_BLOG_POSTS if p["slug"] == slug), None)
    if not current:
        return SEED_BLOG_POSTS[:limit]

    current_tags = set((current.get("tags") or "").split(","))
    scored: list[tuple[int, dict]] = []

    for post in SEED_BLOG_POSTS:
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
        for post in SEED_BLOG_POSTS:
            if post["slug"] != slug and post not in related:
                related.append(post)
            if len(related) >= limit:
                break

    return related[:limit]
