"""Calculator service dispatcher."""

from app.services.calculators import amazon_fee, fba_profit, shipping, vat

CALCULATORS = {
    "amazon-fee-calculator": amazon_fee.calculate,
    "fba-profit-calculator": fba_profit.calculate,
    "vat-calculator": vat.calculate,
    "shipping-calculator": shipping.calculate,
}


def run_calculator(slug: str, data: dict) -> dict:
    """Run calculator by tool slug. Raises ValueError if not found."""
    fn = CALCULATORS.get(slug)
    if not fn:
        raise ValueError(f"No calculator for slug: {slug}")
    return fn(data)
