"""Tool calculation and AI generation API."""

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse

from app.services.ai_service import generate_product_description, generate_review_reply
from app.services.calculator_service import run_calculator
from app.services.tools_service import get_tool_by_slug

router = APIRouter(prefix="/api/tools", tags=["api"])

AI_TOOLS = {
    "negative-review-reply": generate_review_reply,
    "product-description-generator": generate_product_description,
}


@router.post("/{slug}/run")
async def run_tool(slug: str, request: Request) -> JSONResponse:
    """Execute calculator or AI tool."""
    tool = get_tool_by_slug(slug)
    if not tool:
        raise HTTPException(status_code=404, detail="Tool not found")

    data = await request.json()

    # Calculator tools
    if slug in ("amazon-fee-calculator", "fba-profit-calculator", "vat-calculator", "shipping-calculator"):
        try:
            result = run_calculator(slug, data)
            return JSONResponse({"success": True, "result": result})
        except (ValueError, TypeError) as exc:
            return JSONResponse({"success": False, "error": str(exc)}, status_code=400)

    # AI tools
    if slug == "negative-review-reply":
        text = await generate_review_reply(
            data.get("review_text", ""),
            data.get("product_name", ""),
            data.get("tone", "professional"),
        )
        return JSONResponse({"success": True, "result": {"text": text}})

    if slug == "product-description-generator":
        text = await generate_product_description(
            data.get("product_name", ""),
            data.get("features", ""),
            data.get("platform", "amazon"),
            data.get("tone", "professional"),
        )
        return JSONResponse({"success": True, "result": {"text": text}})

    return JSONResponse(
        {"success": False, "error": "This tool is not yet available."},
        status_code=501,
    )
