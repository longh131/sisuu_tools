"""FBA profit calculator — local computation."""


def calculate(data: dict) -> dict:
    """Calculate FBA profit from input data."""
    sale_price = float(data.get("sale_price", 0))
    product_cost = float(data.get("product_cost", 0))
    amazon_fees = float(data.get("amazon_fees", 0))
    shipping_cost = float(data.get("shipping_cost") or 0)
    other_costs = float(data.get("other_costs") or 0)

    total_costs = product_cost + amazon_fees + shipping_cost + other_costs
    net_profit = round(sale_price - total_costs, 2)
    profit_margin = round((net_profit / sale_price * 100) if sale_price > 0 else 0, 1)
    roi = round((net_profit / total_costs * 100) if total_costs > 0 else 0, 1)

    return {
        "sale_price": sale_price,
        "total_costs": round(total_costs, 2),
        "net_profit": net_profit,
        "profit_margin": profit_margin,
        "roi": roi,
        "summary": (
            f"Net profit: ${net_profit:.2f} | "
            f"Margin: {profit_margin}% | ROI: {roi}%"
        ),
    }
