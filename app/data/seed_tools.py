"""
Expanded tool seed data — all categories per docs/06-工具中心.md
"""

SEED_TOOLS: list[dict] = [
    # ── Calculators (MVP) ──
    {"name": "Amazon Fee Calculator", "slug": "amazon-fee-calculator",
     "description": "Calculate Amazon referral and FBA fees instantly.",
     "intro": "Calculate your Amazon selling fees instantly.",
     "icon": "calculator", "category": "calculators", "is_ai": False,
     "is_popular": True, "is_featured": True, "sort_order": 1},
    {"name": "FBA Profit Calculator", "slug": "fba-profit-calculator",
     "description": "Estimate your Amazon FBA profit margins accurately.",
     "intro": "Estimate your FBA profit margin in seconds.",
     "icon": "trending-up", "category": "calculators", "is_ai": False,
     "is_popular": True, "is_featured": True, "sort_order": 2},
    {"name": "VAT Calculator", "slug": "vat-calculator",
     "description": "Calculate VAT for UK, EU, and international sales.",
     "intro": "Calculate VAT for cross-border eCommerce sales.",
     "icon": "percent", "category": "calculators", "is_ai": False,
     "is_popular": True, "is_featured": True, "sort_order": 3},
    {"name": "Shipping Calculator", "slug": "shipping-calculator",
     "description": "Compare shipping costs across carriers and zones.",
     "intro": "Estimate shipping costs for your eCommerce orders.",
     "icon": "truck", "category": "calculators", "is_ai": False,
     "is_popular": True, "is_featured": False, "sort_order": 4},
    # ── AI Tools (MVP) ──
    {"name": "Review Reply Generator", "slug": "negative-review-reply",
     "description": "Generate professional replies to negative reviews with AI.",
     "intro": "Create professional replies to negative customer reviews.",
     "icon": "message-square", "category": "ai-tools", "is_ai": True,
     "is_popular": True, "is_featured": True, "sort_order": 5},
    {"name": "Product Description Generator", "slug": "product-description-generator",
     "description": "Create compelling product descriptions for any marketplace.",
     "intro": "Generate SEO-friendly product descriptions with AI.",
     "icon": "file-text", "category": "ai-tools", "is_ai": True,
     "is_popular": True, "is_featured": True, "sort_order": 6},
    {"name": "Refund Reply Generator", "slug": "refund-reply-generator",
     "description": "Write professional refund response messages with AI.",
     "intro": "Generate polite and professional refund replies.",
     "icon": "rotate-ccw", "category": "ai-tools", "is_ai": True,
     "is_popular": False, "is_featured": False, "sort_order": 7},
    {"name": "Buyer Message Generator", "slug": "buyer-message-generator",
     "description": "Craft professional buyer messages for any situation.",
     "intro": "Write clear buyer messages for Amazon and eBay.",
     "icon": "mail", "category": "ai-tools", "is_ai": True,
     "is_popular": False, "is_featured": False, "sort_order": 8},
    # ── Policy Center ──
    {"name": "Amazon Policy", "slug": "amazon-policy",
     "description": "Amazon seller policies, rules and account health guidelines.",
     "intro": "Browse Amazon seller policies and compliance rules.",
     "icon": "book-open", "category": "policy", "is_ai": False,
     "is_popular": False, "is_featured": False, "sort_order": 9},
    {"name": "eBay Policy", "slug": "ebay-policy",
     "description": "eBay seller policies, returns and listing rules.",
     "intro": "Browse eBay seller policies and listing requirements.",
     "icon": "book-open", "category": "policy", "is_ai": False,
     "is_popular": False, "is_featured": False, "sort_order": 10},
    {"name": "Walmart Policy", "slug": "walmart-policy",
     "description": "Walmart Marketplace seller policies and guidelines.",
     "intro": "Browse Walmart Marketplace seller policies.",
     "icon": "book-open", "category": "policy", "is_ai": False,
     "is_popular": False, "is_featured": False, "sort_order": 11},
    {"name": "TikTok Shop Policy", "slug": "tiktok-shop-policy",
     "description": "TikTok Shop seller policies and community guidelines.",
     "intro": "Browse TikTok Shop seller policies and rules.",
     "icon": "book-open", "category": "policy", "is_ai": False,
     "is_popular": False, "is_featured": False, "sort_order": 12},
    # ── Seller Resources ──
    {"name": "Seller Templates", "slug": "seller-templates",
     "description": "Free templates for listings, emails and seller operations.",
     "intro": "Download free seller templates for daily operations.",
     "icon": "file", "category": "seller-resources", "is_ai": False,
     "is_popular": False, "is_featured": False, "sort_order": 13},
    {"name": "Seller Checklists", "slug": "seller-checklists",
     "description": "Step-by-step checklists for launching and managing stores.",
     "intro": "Use proven checklists to launch and grow your store.",
     "icon": "check-square", "category": "seller-resources", "is_ai": False,
     "is_popular": False, "is_featured": False, "sort_order": 14},
    {"name": "Seller Guides", "slug": "seller-guides",
     "description": "Comprehensive guides for Amazon, eBay and Shopify sellers.",
     "intro": "Read expert guides for global eCommerce sellers.",
     "icon": "book", "category": "seller-resources", "is_ai": False,
     "is_popular": False, "is_featured": False, "sort_order": 15},
    {"name": "Seller Glossary", "slug": "seller-glossary",
     "description": "eCommerce and marketplace terminology explained.",
     "intro": "Look up eCommerce terms and marketplace jargon.",
     "icon": "list", "category": "seller-resources", "is_ai": False,
     "is_popular": False, "is_featured": False, "sort_order": 16},
]

TOOLS_PER_PAGE = 12


def get_popular_tools(limit: int = 6) -> list[dict]:
    """Return popular tools sorted by sort_order."""
    popular = [t for t in SEED_TOOLS if t.get("is_popular")]
    return sorted(popular, key=lambda t: t.get("sort_order", 99))[:limit]


def get_latest_tools(limit: int = 4) -> list[dict]:
    """Return newest tools by sort_order desc."""
    return sorted(SEED_TOOLS, key=lambda t: t.get("sort_order", 99), reverse=True)[:limit]
