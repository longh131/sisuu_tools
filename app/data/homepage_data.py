"""
Homepage static data for MVP.
Per docs/04-首页开发.md — seed data only, no database queries.
"""

from app.services.tools_service import get_latest_tools_list, get_popular_tools_list

# Re-export tool lists from seed module (single source of truth)
POPULAR_TOOLS = get_popular_tools_list()
LATEST_TOOLS = get_latest_tools_list(4)

# Hero preview items — top 3 popular tools from seed
HERO_PREVIEW_ITEMS = POPULAR_TOOLS[:3]
HERO_PREVIEW_RESULT = "Result: $12.47 profit margin"

# Hero trust and rating — unified data object for component rendering
HERO_TRUST: dict[str, str] = {
    "trust_text": "Trusted by global eCommerce sellers.",
    "rating_stars": "★★★★★",
    "rating_text": "Thousands of sellers use our tools every month.",
}

# Tool categories for homepage section
TOOL_CATEGORIES: list[dict] = [
    {
        "name": "AI Tools",
        "slug": "ai-tools",
        "description": "AI-powered tools for listings, reviews, and customer communication.",
        "icon": "sparkles",
    },
    {
        "name": "Calculators",
        "slug": "calculators",
        "description": "Fee, profit, VAT, and shipping calculators for sellers.",
        "icon": "calculator",
    },
    {
        "name": "Policy Center",
        "slug": "policy",
        "description": "Platform policies for Amazon, eBay, Walmart, and more.",
        "icon": "book-open",
    },
    {
        "name": "Seller Resources",
        "slug": "seller-resources",
        "description": "Guides, templates, checklists, and seller knowledge base.",
        "icon": "folder-open",
    },
]

# Why Choose Seller Toolkit — four advantages
WHY_CHOOSE_ITEMS: list[dict] = [
    {
        "title": "Fast",
        "description": "All tools load instantly and deliver results in seconds.",
        "icon": "zap",
    },
    {
        "title": "Professional",
        "description": "Accurate calculations and AI outputs you can trust.",
        "icon": "award",
    },
    {
        "title": "Free",
        "description": "Most tools are completely free with no registration required.",
        "icon": "gift",
    },
    {
        "title": "Always Updated",
        "description": "We continuously update tools to match latest platform rules.",
        "icon": "refresh-cw",
    },
]

# Homepage FAQ — minimum 6 items per docs/04
FAQ_ITEMS: list[dict] = [
    {
        "question": "What is Seller Toolkit?",
        "answer": (
            "Seller Toolkit is a free online platform that provides practical tools "
            "for global eCommerce sellers, including calculators, AI tools, and policy resources."
        ),
    },
    {
        "question": "Are these tools free?",
        "answer": (
            "Yes, most tools on Seller Toolkit are completely free to use. "
            "No registration is required for the majority of our tools."
        ),
    },
    {
        "question": "Can I use them for Amazon?",
        "answer": (
            "Absolutely. Our tools are designed specifically for Amazon sellers, "
            "as well as sellers on eBay, Shopify, Walmart, Etsy, and TikTok Shop."
        ),
    },
    {
        "question": "Do I need to register?",
        "answer": (
            "No registration is required to use our free tools. "
            "Simply visit the tool page and start using it immediately."
        ),
    },
    {
        "question": "Are AI tools free?",
        "answer": (
            "AI tools offer free usage with daily limits. "
            "Premium usage packages will be available in a future update."
        ),
    },
    {
        "question": "How often are tools updated?",
        "answer": (
            "We regularly update our tools to reflect the latest marketplace fees, "
            "policies, and best practices. Check back often for new tools and improvements."
        ),
    },
]
