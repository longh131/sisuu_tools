"""Usage tier limits — extensible for future membership system."""

# Tier daily limits for AI tools (-1 = unlimited)
TIER_LIMITS: dict[str, int] = {
    "guest": 3,
    "registered": 10,
    "pro": 100,
    "business": -1,
}

# Future membership integration hook
MEMBERSHIP_TIERS = ("guest", "registered", "pro", "business")
