"""
AI prompt templates for all AI tools.
Centralised for maintainability — each tool maps to system + prompt builder.
"""

from typing import Callable


def _tone(data: dict, default: str = "professional") -> str:
    return data.get("tone") or default


def _platform(data: dict, default: str = "amazon") -> str:
    return data.get("platform") or default


# slug -> {system, build_prompt}
AI_TOOL_PROMPTS: dict[str, dict] = {}


def _register(slug: str, system: str, build_prompt: Callable[[dict], str]) -> None:
    AI_TOOL_PROMPTS[slug] = {"system": system, "build_prompt": build_prompt}


def _review_reply_prompt(d: dict) -> str:
    extra = f" for product: {d.get('product_name', '')}" if d.get("product_name") else ""
    return f"Write a {_tone(d)} reply to this negative review{extra}:\n\n\"{d.get('review_text', '')}\""


_register(
    "negative-review-reply",
    "You are a professional eCommerce customer service expert. Write empathetic, professional replies to negative reviews. Keep under 150 words. Never be defensive.",
    _review_reply_prompt,
)

_register(
    "product-description-generator",
    "You are an expert marketplace copywriter. Write SEO-optimized product descriptions with bullet points. Keep under 300 words.",
    lambda d: f"Write a {_tone(d)} product description for {_platform(d)}.\nProduct: {d.get('product_name', '')}\nFeatures: {d.get('features', '')}",
)

_register(
    "refund-reply-generator",
    "You are an eCommerce customer service expert. Write polite, professional refund response messages. Keep under 120 words.",
    lambda d: f"Write a {_tone(d)} refund reply for {_platform(d)}.\nCustomer message: {d.get('customer_message', '')}\nRefund reason: {d.get('refund_reason', '')}",
)

_register(
    "buyer-message-generator",
    "You are an eCommerce communication expert. Write clear, professional buyer messages for marketplace sellers.",
    lambda d: f"Write a {_tone(d)} buyer message for {_platform(d)}.\nSituation: {d.get('situation', '')}\nKey points: {d.get('key_points', '')}",
)

_register(
    "customer-service-reply-generator",
    "You are a senior eCommerce customer support specialist. Write helpful, brand-safe customer service replies.",
    lambda d: f"Write a {_tone(d)} customer service reply for {_platform(d)}.\nCustomer inquiry: {d.get('inquiry', '')}\nContext: {d.get('context', '')}",
)

_register(
    "product-title-generator",
    "You are an Amazon SEO expert. Generate compelling, keyword-rich product titles under 200 characters.",
    lambda d: f"Generate 3 {_tone(d)} product titles for {_platform(d)}.\nProduct: {d.get('product_name', '')}\nKeywords: {d.get('keywords', '')}\nCategory: {d.get('category', '')}",
)

_register(
    "bullet-point-generator",
    "You are an Amazon listing expert. Write persuasive bullet points following Amazon best practices. Max 5 bullets.",
    lambda d: f"Write 5 bullet points for {_platform(d)} listing.\nProduct: {d.get('product_name', '')}\nFeatures: {d.get('features', '')}\nTone: {_tone(d)}",
)

_register(
    "amazon-listing-optimizer",
    "You are an Amazon listing optimization consultant. Analyze and improve listings for conversion and SEO.",
    lambda d: f"Optimize this Amazon listing:\nTitle: {d.get('title', '')}\nBullets: {d.get('bullets', '')}\nDescription: {d.get('description', '')}\nProvide improved title, bullets and key recommendations.",
)

_register(
    "keyword-generator",
    "You are an eCommerce SEO keyword researcher. Generate relevant, high-intent keywords for marketplace listings.",
    lambda d: f"Generate 20 SEO keywords for {_platform(d)}.\nProduct: {d.get('product_name', '')}\nCategory: {d.get('category', '')}\nTarget market: {d.get('market', 'US')}",
)

_register(
    "review-response-generator",
    "You are a customer experience expert. Write professional responses to customer reviews of any sentiment.",
    lambda d: f"Write a {_tone(d)} response to this review for {_platform(d)}:\n\n\"{d.get('review_text', '')}\"",
)

_register(
    "ad-copy-generator",
    "You are a PPC advertising copywriter for eCommerce. Write compelling ad copy with clear CTAs.",
    lambda d: f"Write 3 ad copy variations for {_platform(d)} PPC.\nProduct: {d.get('product_name', '')}\nUSP: {d.get('usp', '')}\nTone: {_tone(d)}",
)

_register(
    "email-subject-generator",
    "You are an email marketing expert for eCommerce sellers. Write high-open-rate subject lines.",
    lambda d: f"Generate 5 email subject lines.\nPurpose: {d.get('purpose', '')}\nAudience: {d.get('audience', 'eCommerce buyers')}\nTone: {_tone(d)}",
)

_register(
    "social-post-generator",
    "You are a social media manager for eCommerce brands. Write engaging posts for product promotion.",
    lambda d: f"Write a social media post for {d.get('platform', 'Instagram')}.\nProduct: {d.get('product_name', '')}\nAngle: {d.get('angle', 'product launch')}\nTone: {_tone(d)}",
)

_register(
    "thank-you-message-generator",
    "You are an eCommerce seller communication expert. Write warm, professional thank-you messages.",
    lambda d: f"Write a thank-you message for {_platform(d)}.\nOccasion: {d.get('occasion', 'order completion')}\nTone: {_tone(d)}",
)

_register(
    "return-request-reply-generator",
    "You are a returns management specialist. Write professional replies to return requests.",
    lambda d: f"Write a {_tone(d)} reply to this return request on {_platform(d)}:\n{d.get('return_message', '')}",
)

_register(
    "order-delay-message-generator",
    "You are a customer communication expert. Write apologetic, reassuring delay notification messages.",
    lambda d: f"Write an order delay message for {_platform(d)}.\nDelay reason: {d.get('delay_reason', '')}\nNew ETA: {d.get('new_eta', '')}\nTone: {_tone(d)}",
)

_register(
    "ebay-listing-generator",
    "You are an eBay listing expert. Write complete eBay listing content with title, description and item specifics suggestions.",
    lambda d: f"Create an eBay listing.\nProduct: {d.get('product_name', '')}\nCondition: {d.get('condition', 'New')}\nFeatures: {d.get('features', '')}",
)

_register(
    "etsy-listing-generator",
    "You are an Etsy SEO expert. Write handmade-friendly Etsy listing content with tags.",
    lambda d: f"Create an Etsy listing.\nProduct: {d.get('product_name', '')}\nMaterials: {d.get('materials', '')}\nFeatures: {d.get('features', '')}",
)

AI_TOOL_SLUGS: set[str] = set(AI_TOOL_PROMPTS.keys())
