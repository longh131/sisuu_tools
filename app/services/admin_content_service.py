"""Admin CRUD for tools and blog posts."""

from datetime import datetime

from sqlalchemy.orm import Session, joinedload

from app.models.blog_post import BlogPost
from app.models.tool import Tool
from app.models.tool_category import ToolCategory


def _tool_dict(row: Tool) -> dict:
    return {
        "id": row.id,
        "name": row.name,
        "slug": row.slug,
        "description": row.description or "",
        "category": row.category.slug if row.category else "",
        "category_name": row.category.name if row.category else "",
        "is_ai": row.is_ai,
        "is_popular": row.is_popular,
        "is_featured": row.is_featured,
        "sort_order": row.sort_order,
        "status": row.status,
    }


def list_tools_admin(db: Session) -> list[dict]:
    rows = db.query(Tool).options(joinedload(Tool.category)).order_by(Tool.sort_order).all()
    return [_tool_dict(r) for r in rows]


def get_tool_admin(db: Session, tool_id: int) -> Tool | None:
    return db.query(Tool).options(joinedload(Tool.category)).filter(Tool.id == tool_id).first()


def create_tool(db: Session, data: dict) -> Tool:
    tool = Tool(
        category_id=data["category_id"],
        name=data["name"],
        slug=data["slug"],
        description=data.get("description", ""),
        intro=data.get("intro", data.get("description", "")),
        icon=data.get("icon", "wrench"),
        is_ai=data.get("is_ai", False),
        is_popular=data.get("is_popular", False),
        is_featured=data.get("is_featured", False),
        sort_order=data.get("sort_order", 99),
        status=data.get("status", True),
    )
    db.add(tool)
    db.commit()
    db.refresh(tool)
    return tool


def update_tool(db: Session, tool: Tool, data: dict) -> Tool:
    for key in ("category_id", "name", "slug", "description", "intro", "icon",
                "is_ai", "is_popular", "is_featured", "sort_order", "status"):
        if key in data:
            setattr(tool, key, data[key])
    db.commit()
    db.refresh(tool)
    return tool


def delete_tool(db: Session, tool: Tool) -> None:
    tool.status = False
    db.commit()


def list_categories_admin(db: Session) -> list[ToolCategory]:
    return db.query(ToolCategory).order_by(ToolCategory.sort_order).all()


def _blog_dict(row: BlogPost) -> dict:
    return {
        "id": row.id,
        "title": row.title,
        "slug": row.slug,
        "summary": row.summary or "",
        "category": row.category or "",
        "published_date": row.published_at.strftime("%Y-%m-%d") if row.published_at else "",
        "status": "published" if row.published_at else "draft",
    }


def list_blog_admin(db: Session) -> list[dict]:
    rows = db.query(BlogPost).order_by(BlogPost.published_at.desc()).all()
    return [_blog_dict(r) for r in rows]


def get_blog_admin(db: Session, post_id: int) -> BlogPost | None:
    return db.query(BlogPost).filter(BlogPost.id == post_id).first()


def create_blog_post(db: Session, data: dict) -> BlogPost:
    published = data.get("publish", False)
    post = BlogPost(
        title=data["title"],
        slug=data["slug"],
        summary=data.get("summary", ""),
        content=data.get("content", ""),
        category=data.get("category", ""),
        tags=data.get("tags", ""),
        seo_title=data.get("seo_title", ""),
        seo_description=data.get("seo_description", ""),
        published_at=datetime.utcnow() if published else None,
    )
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


def update_blog_post(db: Session, post: BlogPost, data: dict) -> BlogPost:
    post.title = data.get("title", post.title)
    post.slug = data.get("slug", post.slug)
    post.summary = data.get("summary", post.summary)
    post.content = data.get("content", post.content)
    post.category = data.get("category", post.category)
    post.tags = data.get("tags", post.tags)
    post.seo_title = data.get("seo_title", post.seo_title)
    post.seo_description = data.get("seo_description", post.seo_description)
    if data.get("publish") and not post.published_at:
        post.published_at = datetime.utcnow()
    if data.get("unpublish"):
        post.published_at = None
    db.commit()
    db.refresh(post)
    return post


def delete_blog_post(db: Session, post: BlogPost) -> None:
    db.delete(post)
    db.commit()
