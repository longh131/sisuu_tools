"""
DeepSeek AI service.
API Key loaded from .env — never hardcoded.
"""

import httpx

from app.config import get_settings
from app.data.ai_prompts import AI_TOOL_PROMPTS

settings = get_settings()


async def generate_text(prompt: str, system: str = "") -> str:
    """Call DeepSeek API. Returns generated text or fallback message."""
    if not settings.deepseek_api_key:
        return (
            "AI generation requires a DeepSeek API key. "
            "Please configure DEEPSEEK_API_KEY in your .env file."
        )

    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{settings.deepseek_api_base}/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {settings.deepseek_api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "deepseek-chat",
                    "messages": messages,
                    "max_tokens": 1000,
                    "temperature": 0.7,
                },
            )
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]
    except Exception as exc:
        return f"AI generation failed. Please try again later. ({type(exc).__name__})"


async def run_ai_tool(slug: str, data: dict) -> str:
    """Run any registered AI tool by slug."""
    config = AI_TOOL_PROMPTS.get(slug)
    if not config:
        raise ValueError(f"No AI prompt configured for: {slug}")
    prompt = config["build_prompt"](data)
    return await generate_text(prompt, config["system"])
