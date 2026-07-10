"""Calculator service dispatcher."""

from app.services.calculators import amazon_fee, fba_profit, marketplace, shipping, vat

CALCULATORS = {
    "amazon-fee-calculator": amazon_fee.calculate,
    "fba-profit-calculator": fba_profit.calculate,
    "vat-calculator": vat.calculate,
    "shipping-calculator": shipping.calculate,
    "ebay-fee-calculator": marketplace.ebay_fee,
    "shopify-fee-calculator": marketplace.shopify_fee,
    "etsy-fee-calculator": marketplace.etsy_fee,
    "profit-margin-calculator": marketplace.profit_margin,
    "break-even-calculator": marketplace.break_even,
    "roi-calculator": marketplace.roi_calc,
    "ppc-cost-calculator": marketplace.ppc_cost,
    "discount-calculator": marketplace.discount_calc,
    "price-markup-calculator": marketplace.price_markup,
    "unit-economics-calculator": marketplace.unit_economics,
}


def run_calculator(slug: str, data: dict) -> dict:
    """Run calculator by tool slug. Raises ValueError if not found."""
    fn = CALCULATORS.get(slug)
    if not fn:
        raise ValueError(f"No calculator for slug: {slug}")
    return fn(data)
