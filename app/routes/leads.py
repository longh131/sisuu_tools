"""Lead capture and usage status API."""

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from app.services.lead_service import save_lead, validate_email
from app.services.usage_service import check_ai_limit, set_user_tier

router = APIRouter(prefix="/api", tags=["api"])


class SubscribeRequest(BaseModel):
    email: str = Field(..., max_length=255)
    source: str = Field(default="other", max_length=50)


@router.post("/leads/subscribe")
async def subscribe(request: Request, body: SubscribeRequest) -> JSONResponse:
    """Capture email lead and upgrade visitor to registered tier."""
    error = validate_email(body.email)
    if error:
        return JSONResponse({"success": False, "error": error}, status_code=400)

    success, message = save_lead(body.email, body.source)
    if success:
        set_user_tier(request, "registered")

    usage = check_ai_limit(request)
    return JSONResponse({
        "success": success,
        "message": message,
        "tier": usage["tier"],
        "limit": usage["limit"],
        "remaining": usage["remaining"],
    })


@router.get("/usage/status")
async def usage_status(request: Request) -> JSONResponse:
    """Return current AI usage status for frontend."""
    status = check_ai_limit(request)
    return JSONResponse({"success": True, **status})
