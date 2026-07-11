"""Pricing plans — commercial funnel Phase 1."""

PRICING_PAGE = {
    "h1": "Simple, Transparent Pricing",
    "title": "Pricing — Seller Toolkit",
    "description": (
        "Start free with calculators and AI tools. Upgrade to Pro or Business "
        "for higher AI limits and advanced seller tools."
    ),
    "breadcrumb": [{"name": "Home", "url": "/"}, {"name": "Pricing", "url": ""}],
}

PRICING_PLANS: list[dict] = [
    {
        "id": "free",
        "name": "Free",
        "price": "$0",
        "period": "forever",
        "description": "Perfect for new sellers getting started.",
        "features": [
            "All calculator tools — unlimited",
            "AI tools — 3 uses per day",
            "Policy & resource pages",
            "Blog & seller guides",
            "No credit card required",
        ],
        "cta_text": "Start Free",
        "cta_url": "/tools",
        "cta_style": "outline",
        "highlighted": False,
    },
    {
        "id": "pro",
        "name": "Pro",
        "price": "$19",
        "period": "/month",
        "description": "For active sellers who use AI tools daily.",
        "features": [
            "Everything in Free",
            "AI tools — 100 uses per day",
            "Advanced AI listing tools",
            "Priority new tool access",
            "Email support",
        ],
        "cta_text": "Upgrade Now",
        "cta_url": "/contact?plan=pro",
        "cta_style": "primary",
        "highlighted": True,
        "badge": "Most Popular",
        "coming_soon": True,
    },
    {
        "id": "business",
        "name": "Business",
        "price": "$49",
        "period": "/month",
        "description": "For teams and high-volume sellers.",
        "features": [
            "Everything in Pro",
            "AI tools — unlimited",
            "Team access (up to 5 seats)",
            "API access (coming soon)",
            "Dedicated support",
        ],
        "cta_text": "Upgrade Now",
        "cta_url": "/contact?plan=business",
        "cta_style": "outline",
        "highlighted": False,
        "coming_soon": True,
    },
]

PRICING_FAQ: list[dict] = [
    {
        "question": "Can I use Seller Toolkit for free?",
        "answer": "Yes. All calculators and basic AI tools are free. Free users get 3 AI generations per day. Subscribe with your email to unlock 10 daily AI uses.",
    },
    {
        "question": "When will Pro and Business plans launch?",
        "answer": "Pro ($19/month) and Business ($49/month) are coming soon. Click Upgrade to join the waitlist — we will notify you when payments go live. No charge until then.",
    },
    {
        "question": "Do I need a credit card to start?",
        "answer": "No. Start using all free tools instantly without registration or payment.",
    },
    {
        "question": "What happens when I hit my daily AI limit?",
        "answer": "You can subscribe with your email for more free uses, or upgrade to Pro when available. Limits reset at midnight UTC.",
    },
]
