"""
Tool category metadata for Tool Center.
Per docs/06-工具中心.md
"""

TOOL_CATEGORIES: dict[str, dict] = {
    "ai-tools": {
        "name": "AI Tools",
        "slug": "ai-tools",
        "description": (
            "AI-powered tools designed to help eCommerce sellers write faster, "
            "respond smarter and improve productivity."
        ),
        "icon": "sparkles",
    },
    "calculators": {
        "name": "Calculators",
        "slug": "calculators",
        "description": (
            "Free calculators for Amazon fees, FBA profit, VAT, shipping and more."
        ),
        "icon": "calculator",
    },
    "policy": {
        "name": "Policy Center",
        "slug": "policy",
        "description": (
            "Platform policies and rules for Amazon, eBay, Walmart, and TikTok Shop sellers."
        ),
        "icon": "book-open",
    },
    "seller-resources": {
        "name": "Seller Resources",
        "slug": "seller-resources",
        "description": (
            "Free seller guides, templates, checklists and glossary for eCommerce sellers."
        ),
        "icon": "folder-open",
    },
}

# Ordered list for category tabs navigation
CATEGORY_TAB_ORDER: list[str] = ["ai-tools", "calculators", "policy", "seller-resources"]
