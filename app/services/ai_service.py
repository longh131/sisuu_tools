"""
DeepSeek AI service.
API Key loaded from .env — never hardcoded.
"""

import httpx

from app.config import get_settings

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


async def generate_review_reply(review_text: str, product_name: str, tone: str) -> str:
    """Generate a professional review reply."""
    system = (
        "You are a professional eCommerce customer service expert. "
        "Write empathetic, professional replies to negative customer reviews. "
        "Keep replies concise (under 150 words). Never be defensive."
    )
    prompt = (
        f"Write a {tone} reply to this negative review"
        f"{f' for product: {product_name}' if product_name else ''}:\n\n"
        f'"{review_text}"'
    )
    return await generate_text(prompt, system)


async def generate_product_description(
    product_name: str, features: str, platform: str, tone: str
) -> str:
    """Generate a product description."""
    system = (
        f"You are an expert {platform} listing copywriter. "
        "Write SEO-optimized product descriptions. "
        "Use bullet points for features. Keep under 300 words."
    )
    prompt = (
        f"Write a {tone} product description for {platform}.\n"
        f"Product: {product_name}\n"
        f"Features: {features}"
    )
    return await generate_text(prompt, system)
