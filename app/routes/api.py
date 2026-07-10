"""Tool calculation and AI generation API."""

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse

from app.data.ai_prompts import AI_TOOL_SLUGS
from app.services.ai_service import run_ai_tool
from app.services.calculator_service import CALCULATORS, run_calculator
from app.services.tools_service import get_tool_by_slug
from app.services.usage_service import (
    check_ai_limit,
    limit_exceeded_message,
    record_ai_usage,
)

router = APIRouter(prefix="/api/tools", tags=["api"])


@router.post("/{slug}/run")
async def run_tool(slug: str, request: Request) -> JSONResponse:
    """Execute calculator or AI tool with usage limits."""
    tool = get_tool_by_slug(slug)
    if not tool:
        raise HTTPException(status_code=404, detail="Tool not found")

    data = await request.json()

    # Calculator tools — unlimited for all tiers
    if slug in CALCULATORS:
        try:
            result = run_calculator(slug, data)
            return JSONResponse({"success": True, "result": result})
        except (ValueError, TypeError) as exc:
            return JSONResponse({"success": False, "error": str(exc)}, status_code=400)

    # AI tools — check daily usage limit
    if slug in AI_TOOL_SLUGS or tool.get("is_ai"):
        status = check_ai_limit(request)
        if not status["allowed"]:
            return JSONResponse({
                "success": False,
                "error": limit_exceeded_message(status),
                "limit_reached": True,
                "usage": status,
            }, status_code=429)

        try:
            text = await run_ai_tool(slug, data)
            record_ai_usage(request, slug)
            updated = check_ai_limit(request)
            return JSONResponse({
                "success": True,
                "result": {"text": text},
                "usage": updated,
            })
        except ValueError as exc:
            return JSONResponse({"success": False, "error": str(exc)}, status_code=400)

    return JSONResponse(
        {"success": False, "error": "This tool is not yet available."},
        status_code=501,
    )
