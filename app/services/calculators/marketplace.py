"""Marketplace and business calculators — commercial phase."""

from app.services.calculators import amazon_fee


def ebay_fee(data: dict) -> dict:
    price = float(data.get("sale_price", 0))
    category = data.get("category", "general")
    rates = {"general": 0.129, "electronics": 0.129, "clothing": 0.129, "collectibles": 0.129}
    rate = rates.get(category, 0.129)
    fee = round(price * rate, 2)
    net = round(price - fee, 2)
    return {
        "summary": f"eBay fee estimate: ${fee:.2f} ({rate*100:.1f}%)",
        "sale_price": f"${price:.2f}",
        "ebay_fee": f"${fee:.2f}",
        "fee_rate": f"{rate*100:.1f}%",
        "net_revenue": f"${net:.2f}",
    }


def shopify_fee(data: dict) -> dict:
    price = float(data.get("sale_price", 0))
    plan = data.get("plan", "basic")
    rates = {"basic": 0.029, "shopify": 0.026, "advanced": 0.024}
    rate = rates.get(plan, 0.029)
    fixed = 0.30
    fee = round(price * rate + fixed, 2)
    net = round(price - fee, 2)
    return {
        "summary": f"Shopify payment fee: ${fee:.2f}",
        "sale_price": f"${price:.2f}",
        "transaction_fee": f"${fee:.2f}",
        "fee_rate": f"{rate*100:.1f}% + $0.30",
        "net_revenue": f"${net:.2f}",
    }


def etsy_fee(data: dict) -> dict:
    price = float(data.get("sale_price", 0))
    listing = 0.20
    transaction = round(price * 0.065, 2)
    payment = round(price * 0.03 + 0.25, 2)
    total = round(listing + transaction + payment, 2)
    net = round(price - total, 2)
    return {
        "summary": f"Total Etsy fees: ${total:.2f}",
        "sale_price": f"${price:.2f}",
        "listing_fee": f"${listing:.2f}",
        "transaction_fee": f"${transaction:.2f}",
        "payment_fee": f"${payment:.2f}",
        "total_fees": f"${total:.2f}",
        "net_revenue": f"${net:.2f}",
    }


def profit_margin(data: dict) -> dict:
    revenue = float(data.get("revenue", 0))
    cost = float(data.get("cost", 0))
    profit = revenue - cost
    margin = (profit / revenue * 100) if revenue else 0
    return {
        "summary": f"Profit margin: {margin:.1f}%",
        "revenue": f"${revenue:.2f}",
        "cost": f"${cost:.2f}",
        "profit": f"${profit:.2f}",
        "margin_percent": f"{margin:.1f}%",
    }


def break_even(data: dict) -> dict:
    fixed = float(data.get("fixed_costs", 0))
    price = float(data.get("unit_price", 0))
    variable = float(data.get("variable_cost", 0))
    contribution = price - variable
    units = round(fixed / contribution, 0) if contribution > 0 else 0
    revenue = round(units * price, 2)
    return {
        "summary": f"Break-even: {int(units)} units (${revenue:.2f} revenue)",
        "fixed_costs": f"${fixed:.2f}",
        "unit_price": f"${price:.2f}",
        "variable_cost": f"${variable:.2f}",
        "break_even_units": str(int(units)),
        "break_even_revenue": f"${revenue:.2f}",
    }


def roi_calc(data: dict) -> dict:
    investment = float(data.get("investment", 0))
    returns = float(data.get("returns", 0))
    roi = ((returns - investment) / investment * 100) if investment else 0
    return {
        "summary": f"ROI: {roi:.1f}%",
        "investment": f"${investment:.2f}",
        "returns": f"${returns:.2f}",
        "net_profit": f"${returns - investment:.2f}",
        "roi_percent": f"{roi:.1f}%",
    }


def ppc_cost(data: dict) -> dict:
    budget = float(data.get("daily_budget", 0))
    cpc = float(data.get("cpc", 0))
    conv_rate = float(data.get("conversion_rate", 5)) / 100
    clicks = round(budget / cpc, 0) if cpc else 0
    orders = round(clicks * conv_rate, 1)
    acos_target = float(data.get("acos_target", 25))
    return {
        "summary": f"Est. {int(clicks)} clicks, {orders} orders/day",
        "daily_budget": f"${budget:.2f}",
        "cost_per_click": f"${cpc:.2f}",
        "estimated_clicks": str(int(clicks)),
        "estimated_orders": str(orders),
        "acos_target": f"{acos_target:.0f}%",
    }


def discount_calc(data: dict) -> dict:
    original = float(data.get("original_price", 0))
    discount = float(data.get("discount_percent", 0))
    savings = round(original * discount / 100, 2)
    final = round(original - savings, 2)
    return {
        "summary": f"Sale price: ${final:.2f} ({discount:.0f}% off)",
        "original_price": f"${original:.2f}",
        "discount_percent": f"{discount:.0f}%",
        "savings": f"${savings:.2f}",
        "final_price": f"${final:.2f}",
    }


def price_markup(data: dict) -> dict:
    cost = float(data.get("cost", 0))
    markup = float(data.get("markup_percent", 0))
    price = round(cost * (1 + markup / 100), 2)
    profit = round(price - cost, 2)
    return {
        "summary": f"Selling price: ${price:.2f} ({markup:.0f}% markup)",
        "cost": f"${cost:.2f}",
        "markup_percent": f"{markup:.0f}%",
        "selling_price": f"${price:.2f}",
        "profit_per_unit": f"${profit:.2f}",
    }


def unit_economics(data: dict) -> dict:
    price = float(data.get("sale_price", 0))
    cost = float(data.get("total_cost", 0))
    units = float(data.get("monthly_units", 0))
    profit_unit = price - cost
    monthly = round(profit_unit * units, 2)
    margin = (profit_unit / price * 100) if price else 0
    return {
        "summary": f"Monthly profit: ${monthly:.2f} ({margin:.1f}% margin)",
        "sale_price": f"${price:.2f}",
        "total_cost": f"${cost:.2f}",
        "profit_per_unit": f"${profit_unit:.2f}",
        "monthly_units": str(int(units)),
        "monthly_profit": f"${monthly:.2f}",
        "margin_percent": f"{margin:.1f}%",
    }
