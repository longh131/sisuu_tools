"""Amazon fee calculator — local computation, no AI."""

REFERRAL_RATES = {
    "general": 0.15,
    "electronics": 0.08,
    "clothing": 0.17,
    "beauty": 0.08,
    "home": 0.15,
}

# Simplified FBA fee tiers by weight (USD)
FBA_FEE_TIERS = [
    (0.25, 3.22),
    (0.5, 3.40),
    (1.0, 3.86),
    (2.0, 4.75),
    (3.0, 5.40),
    (5.0, 6.10),
    (10.0, 8.50),
    (20.0, 12.00),
]


def _fba_fee(weight: float) -> float:
    """Estimate FBA fulfillment fee by weight."""
    for max_weight, fee in FBA_FEE_TIERS:
        if weight <= max_weight:
            return fee
    return 15.00


def calculate(data: dict) -> dict:
    """Calculate Amazon fees from input data."""
    sale_price = float(data.get("sale_price", 0))
    category = data.get("category", "general")
    fulfillment = data.get("fulfillment", "fba")
    weight = float(data.get("item_weight") or 1.0)

    referral_rate = REFERRAL_RATES.get(category, 0.15)
    referral_fee = round(sale_price * referral_rate, 2)
    fba_fee = round(_fba_fee(weight), 2) if fulfillment == "fba" else 0.0
    total_fees = round(referral_fee + fba_fee, 2)
    net_revenue = round(sale_price - total_fees, 2)

    return {
        "sale_price": sale_price,
        "referral_fee": referral_fee,
        "referral_rate": f"{referral_rate * 100:.0f}%",
        "fba_fee": fba_fee,
        "total_fees": total_fees,
        "net_revenue": net_revenue,
        "fulfillment": fulfillment.upper(),
        "summary": (
            f"Total Amazon fees: ${total_fees:.2f} "
            f"(Referral: ${referral_fee:.2f}, FBA: ${fba_fee:.2f}). "
            f"Net revenue: ${net_revenue:.2f}"
        ),
    }
