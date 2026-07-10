"""AI tool page configs — merged into TOOL_CONFIGS."""

_PLATFORM_OPTS = [
    {"value": "amazon", "label": "Amazon"},
    {"value": "ebay", "label": "eBay"},
    {"value": "shopify", "label": "Shopify"},
    {"value": "etsy", "label": "Etsy"},
]
_TONE_OPTS = [
    {"value": "professional", "label": "Professional"},
    {"value": "friendly", "label": "Friendly"},
    {"value": "empathetic", "label": "Empathetic"},
]


def _ai(name: str, fields: list, related: list) -> dict:
    """Build standard AI tool config."""
    return {
        "tool_type": "ai",
        "button_text": "Generate",
        "how_it_works": [
            {"step": 1, "title": "Enter Details", "description": "Fill in the required information."},
            {"step": 2, "title": "Click Generate", "description": "AI creates optimized content instantly."},
            {"step": 3, "title": "Copy & Use", "description": "Review, edit and use in your business."},
        ],
        "fields": fields,
        "faqs": [
            {"question": f"What is {name}?", "answer": f"An AI-powered tool that helps eCommerce sellers with {name.lower()}."},
            {"question": "Is this tool free?", "answer": "Yes, with free daily usage limits. Subscribe for more uses or upgrade to Pro."},
            {"question": "Should I edit AI output?", "answer": "Always review and personalize AI content before publishing."},
            {"question": "How many times can I use it?", "answer": "Free users get 3 AI uses per day. Email subscribers get 10. Pro plans offer more."},
            {"question": "Which platforms are supported?", "answer": "Works for Amazon, eBay, Shopify, Etsy and other marketplaces."},
        ],
        "related_slugs": related,
    }


AI_TOOL_CONFIGS: dict[str, dict] = {
    "refund-reply-generator": _ai("Refund Reply Generator", [
        {"name": "customer_message", "label": "Customer Message", "type": "textarea", "placeholder": "Paste customer message...", "required": True, "rows": 4},
        {"name": "refund_reason", "label": "Refund Reason", "type": "text", "placeholder": "e.g. Defective item", "required": False},
        {"name": "platform", "label": "Platform", "type": "select", "required": True, "options": _PLATFORM_OPTS},
        {"name": "tone", "label": "Tone", "type": "select", "required": True, "options": _TONE_OPTS},
    ], ["buyer-message-generator", "customer-service-reply-generator", "negative-review-reply", "amazon-fee-calculator"]),
    "buyer-message-generator": _ai("Buyer Message Generator", [
        {"name": "situation", "label": "Situation", "type": "textarea", "placeholder": "Describe the situation...", "required": True, "rows": 3},
        {"name": "key_points", "label": "Key Points", "type": "textarea", "placeholder": "What to communicate...", "required": True, "rows": 3},
        {"name": "platform", "label": "Platform", "type": "select", "required": True, "options": _PLATFORM_OPTS},
        {"name": "tone", "label": "Tone", "type": "select", "required": True, "options": _TONE_OPTS},
    ], ["refund-reply-generator", "customer-service-reply-generator", "negative-review-reply", "product-description-generator"]),
    "customer-service-reply-generator": _ai("Customer Service Reply", [
        {"name": "inquiry", "label": "Customer Inquiry", "type": "textarea", "placeholder": "Paste customer message...", "required": True, "rows": 4},
        {"name": "context", "label": "Additional Context", "type": "text", "placeholder": "Order details, policies...", "required": False},
        {"name": "platform", "label": "Platform", "type": "select", "required": True, "options": _PLATFORM_OPTS},
        {"name": "tone", "label": "Tone", "type": "select", "required": True, "options": _TONE_OPTS},
    ], ["buyer-message-generator", "refund-reply-generator", "negative-review-reply", "thank-you-message-generator"]),
    "product-title-generator": _ai("Product Title Generator", [
        {"name": "product_name", "label": "Product Name", "type": "text", "placeholder": "e.g. Wireless Earbuds", "required": True},
        {"name": "keywords", "label": "Target Keywords", "type": "text", "placeholder": "bluetooth, noise cancelling...", "required": True},
        {"name": "category", "label": "Category", "type": "text", "placeholder": "Electronics", "required": False},
        {"name": "platform", "label": "Platform", "type": "select", "required": True, "options": _PLATFORM_OPTS},
        {"name": "tone", "label": "Tone", "type": "select", "required": True, "options": _TONE_OPTS},
    ], ["bullet-point-generator", "keyword-generator", "amazon-listing-optimizer", "product-description-generator"]),
    "bullet-point-generator": _ai("Bullet Point Generator", [
        {"name": "product_name", "label": "Product Name", "type": "text", "required": True},
        {"name": "features", "label": "Key Features", "type": "textarea", "required": True, "rows": 4},
        {"name": "platform", "label": "Platform", "type": "select", "required": True, "options": _PLATFORM_OPTS},
        {"name": "tone", "label": "Tone", "type": "select", "required": True, "options": _TONE_OPTS},
    ], ["product-title-generator", "product-description-generator", "amazon-listing-optimizer", "keyword-generator"]),
    "amazon-listing-optimizer": _ai("Amazon Listing Optimizer", [
        {"name": "title", "label": "Current Title", "type": "text", "required": True},
        {"name": "bullets", "label": "Current Bullets", "type": "textarea", "required": True, "rows": 4},
        {"name": "description", "label": "Current Description", "type": "textarea", "required": False, "rows": 4},
    ], ["product-title-generator", "bullet-point-generator", "keyword-generator", "product-description-generator"]),
    "keyword-generator": _ai("Keyword Generator", [
        {"name": "product_name", "label": "Product Name", "type": "text", "required": True},
        {"name": "category", "label": "Category", "type": "text", "required": True},
        {"name": "market", "label": "Target Market", "type": "select", "required": True,
         "options": [{"value": "US", "label": "United States"}, {"value": "UK", "label": "United Kingdom"}, {"value": "EU", "label": "European Union"}]},
        {"name": "platform", "label": "Platform", "type": "select", "required": True, "options": _PLATFORM_OPTS},
    ], ["product-title-generator", "amazon-listing-optimizer", "product-description-generator", "bullet-point-generator"]),
    "review-response-generator": _ai("Review Response Generator", [
        {"name": "review_text", "label": "Customer Review", "type": "textarea", "required": True, "rows": 4},
        {"name": "platform", "label": "Platform", "type": "select", "required": True, "options": _PLATFORM_OPTS},
        {"name": "tone", "label": "Tone", "type": "select", "required": True, "options": _TONE_OPTS},
    ], ["negative-review-reply", "refund-reply-generator", "customer-service-reply-generator", "thank-you-message-generator"]),
    "ad-copy-generator": _ai("Ad Copy Generator", [
        {"name": "product_name", "label": "Product Name", "type": "text", "required": True},
        {"name": "usp", "label": "Unique Selling Point", "type": "text", "required": True},
        {"name": "platform", "label": "Ad Platform", "type": "select", "required": True, "options": _PLATFORM_OPTS},
        {"name": "tone", "label": "Tone", "type": "select", "required": True, "options": _TONE_OPTS},
    ], ["keyword-generator", "product-title-generator", "ppc-cost-calculator", "product-description-generator"]),
    "email-subject-generator": _ai("Email Subject Generator", [
        {"name": "purpose", "label": "Email Purpose", "type": "text", "placeholder": "e.g. Product launch", "required": True},
        {"name": "audience", "label": "Audience", "type": "text", "placeholder": "e.g. Repeat customers", "required": False},
        {"name": "tone", "label": "Tone", "type": "select", "required": True, "options": _TONE_OPTS},
    ], ["buyer-message-generator", "thank-you-message-generator", "ad-copy-generator", "social-post-generator"]),
    "social-post-generator": _ai("Social Post Generator", [
        {"name": "product_name", "label": "Product Name", "type": "text", "required": True},
        {"name": "angle", "label": "Post Angle", "type": "text", "placeholder": "sale, launch, review...", "required": True},
        {"name": "platform", "label": "Social Platform", "type": "select", "required": True,
         "options": [{"value": "Instagram", "label": "Instagram"}, {"value": "Facebook", "label": "Facebook"}, {"value": "TikTok", "label": "TikTok"}, {"value": "Twitter", "label": "X / Twitter"}]},
        {"name": "tone", "label": "Tone", "type": "select", "required": True, "options": _TONE_OPTS},
    ], ["ad-copy-generator", "product-description-generator", "email-subject-generator", "product-title-generator"]),
    "thank-you-message-generator": _ai("Thank You Message Generator", [
        {"name": "occasion", "label": "Occasion", "type": "text", "placeholder": "order, review, repeat purchase", "required": True},
        {"name": "platform", "label": "Platform", "type": "select", "required": True, "options": _PLATFORM_OPTS},
        {"name": "tone", "label": "Tone", "type": "select", "required": True, "options": _TONE_OPTS},
    ], ["buyer-message-generator", "customer-service-reply-generator", "review-response-generator", "order-delay-message-generator"]),
    "return-request-reply-generator": _ai("Return Request Reply", [
        {"name": "return_message", "label": "Return Request", "type": "textarea", "required": True, "rows": 4},
        {"name": "platform", "label": "Platform", "type": "select", "required": True, "options": _PLATFORM_OPTS},
        {"name": "tone", "label": "Tone", "type": "select", "required": True, "options": _TONE_OPTS},
    ], ["refund-reply-generator", "customer-service-reply-generator", "buyer-message-generator", "negative-review-reply"]),
    "order-delay-message-generator": _ai("Order Delay Message", [
        {"name": "delay_reason", "label": "Delay Reason", "type": "text", "required": True},
        {"name": "new_eta", "label": "New ETA", "type": "text", "placeholder": "e.g. 3-5 business days", "required": True},
        {"name": "platform", "label": "Platform", "type": "select", "required": True, "options": _PLATFORM_OPTS},
        {"name": "tone", "label": "Tone", "type": "select", "required": True, "options": _TONE_OPTS},
    ], ["buyer-message-generator", "thank-you-message-generator", "customer-service-reply-generator", "shipping-calculator"]),
    "ebay-listing-generator": _ai("eBay Listing Generator", [
        {"name": "product_name", "label": "Product Name", "type": "text", "required": True},
        {"name": "condition", "label": "Condition", "type": "select", "required": True,
         "options": [{"value": "New", "label": "New"}, {"value": "Used", "label": "Used"}, {"value": "Refurbished", "label": "Refurbished"}]},
        {"name": "features", "label": "Features", "type": "textarea", "required": True, "rows": 4},
    ], ["product-description-generator", "ebay-fee-calculator", "product-title-generator", "bullet-point-generator"]),
    "etsy-listing-generator": _ai("Etsy Listing Generator", [
        {"name": "product_name", "label": "Product Name", "type": "text", "required": True},
        {"name": "materials", "label": "Materials", "type": "text", "required": False},
        {"name": "features", "label": "Features", "type": "textarea", "required": True, "rows": 4},
    ], ["product-description-generator", "etsy-fee-calculator", "keyword-generator", "product-title-generator"]),
}
