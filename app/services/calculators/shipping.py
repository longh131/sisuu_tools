"""Shipping cost calculator — local estimation."""

BASE_RATES = {
    "domestic": {"standard": 5.99, "expedited": 12.99, "express": 24.99},
    "canada": {"standard": 14.99, "expedited": 24.99, "express": 39.99},
    "uk": {"standard": 18.99, "expedited": 32.99, "express": 49.99},
    "eu": {"standard": 22.99, "expedited": 38.99, "express": 59.99},
    "international": {"standard": 28.99, "expedited": 48.99, "express": 79.99},
}

WEIGHT_MULTIPLIER = 0.85  # per lb above 1 lb


def calculate(data: dict) -> dict:
    """Estimate shipping cost from input data."""
    weight = float(data.get("weight", 1.0))
    destination = data.get("destination", "domestic")
    service = data.get("service", "standard")

    base = BASE_RATES.get(destination, BASE_RATES["domestic"]).get(service, 5.99)
    extra_weight = max(0, weight - 1.0)
    weight_surcharge = round(extra_weight * WEIGHT_MULTIPLIER, 2)
    total_cost = round(base + weight_surcharge, 2)

    return {
        "weight": weight,
        "destination": destination.replace("-", " ").title(),
        "service": service.title(),
        "base_rate": base,
        "weight_surcharge": weight_surcharge,
        "total_cost": total_cost,
        "summary": (
            f"Estimated shipping: ${total_cost:.2f} "
            f"({service.title()} to {destination.replace('-', ' ').title()}, {weight} lbs)"
        ),
    }
