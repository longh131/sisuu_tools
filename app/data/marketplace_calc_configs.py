"""Calculator configs for marketplace and business tools."""

_CALC_HOW = [
    {"step": 1, "title": "Enter Values", "description": "Input your product or business data."},
    {"step": 2, "title": "Click Calculate", "description": "Get instant results."},
    {"step": 3, "title": "Review Results", "description": "Use the breakdown for pricing decisions."},
]


def _calc(fields: list, related: list, name: str) -> dict:
    return {
        "tool_type": "calculator",
        "button_text": "Calculate",
        "how_it_works": _CALC_HOW,
        "fields": fields,
        "faqs": [
            {"question": f"What is {name}?", "answer": f"A free calculator for eCommerce sellers."},
            {"question": "Is this tool free?", "answer": "Yes, completely free with unlimited use."},
            {"question": "How accurate are results?", "answer": "Estimates based on standard fee schedules. Verify with official sources."},
            {"question": "Do I need to register?", "answer": "No registration required."},
            {"question": "Can I use this for any marketplace?", "answer": "Designed for the specified marketplace fee structures."},
        ],
        "related_slugs": related,
    }


MARKETPLACE_CALC_CONFIGS: dict[str, dict] = {
    "ebay-fee-calculator": _calc([
        {"name": "sale_price", "label": "Sale Price ($)", "type": "number", "required": True, "min": 0, "step": 0.01},
        {"name": "category", "label": "Category", "type": "select", "required": True,
         "options": [{"value": "general", "label": "General"}, {"value": "electronics", "label": "Electronics"}, {"value": "clothing", "label": "Clothing"}]},
    ], ["amazon-fee-calculator", "shopify-fee-calculator", "profit-margin-calculator", "fba-profit-calculator"], "eBay Fee Calculator"),
    "shopify-fee-calculator": _calc([
        {"name": "sale_price", "label": "Sale Price ($)", "type": "number", "required": True, "min": 0, "step": 0.01},
        {"name": "plan", "label": "Shopify Plan", "type": "select", "required": True,
         "options": [{"value": "basic", "label": "Basic (2.9%)"}, {"value": "shopify", "label": "Shopify (2.6%)"}, {"value": "advanced", "label": "Advanced (2.4%)"}]},
    ], ["ebay-fee-calculator", "etsy-fee-calculator", "profit-margin-calculator", "amazon-fee-calculator"], "Shopify Fee Calculator"),
    "etsy-fee-calculator": _calc([
        {"name": "sale_price", "label": "Sale Price ($)", "type": "number", "required": True, "min": 0, "step": 0.01},
    ], ["ebay-fee-calculator", "shopify-fee-calculator", "profit-margin-calculator", "etsy-listing-generator"], "Etsy Fee Calculator"),
    "profit-margin-calculator": _calc([
        {"name": "revenue", "label": "Revenue ($)", "type": "number", "required": True, "min": 0, "step": 0.01},
        {"name": "cost", "label": "Total Cost ($)", "type": "number", "required": True, "min": 0, "step": 0.01},
    ], ["fba-profit-calculator", "roi-calculator", "break-even-calculator", "amazon-fee-calculator"], "Profit Margin Calculator"),
    "break-even-calculator": _calc([
        {"name": "fixed_costs", "label": "Fixed Costs ($)", "type": "number", "required": True, "min": 0},
        {"name": "unit_price", "label": "Unit Price ($)", "type": "number", "required": True, "min": 0, "step": 0.01},
        {"name": "variable_cost", "label": "Variable Cost per Unit ($)", "type": "number", "required": True, "min": 0, "step": 0.01},
    ], ["profit-margin-calculator", "roi-calculator", "fba-profit-calculator", "unit-economics-calculator"], "Break-Even Calculator"),
    "roi-calculator": _calc([
        {"name": "investment", "label": "Investment ($)", "type": "number", "required": True, "min": 0},
        {"name": "returns", "label": "Returns ($)", "type": "number", "required": True, "min": 0},
    ], ["profit-margin-calculator", "break-even-calculator", "ppc-cost-calculator", "fba-profit-calculator"], "ROI Calculator"),
    "ppc-cost-calculator": _calc([
        {"name": "daily_budget", "label": "Daily Ad Budget ($)", "type": "number", "required": True, "min": 0},
        {"name": "cpc", "label": "Cost per Click ($)", "type": "number", "required": True, "min": 0.01, "step": 0.01},
        {"name": "conversion_rate", "label": "Conversion Rate (%)", "type": "number", "required": True, "min": 0, "max": 100, "step": 0.1},
        {"name": "acos_target", "label": "Target ACOS (%)", "type": "number", "required": False, "min": 0, "step": 1},
    ], ["ad-copy-generator", "amazon-fee-calculator", "profit-margin-calculator", "keyword-generator"], "PPC Cost Calculator"),
    "discount-calculator": _calc([
        {"name": "original_price", "label": "Original Price ($)", "type": "number", "required": True, "min": 0, "step": 0.01},
        {"name": "discount_percent", "label": "Discount (%)", "type": "number", "required": True, "min": 0, "max": 100, "step": 1},
    ], ["price-markup-calculator", "profit-margin-calculator", "amazon-fee-calculator", "fba-profit-calculator"], "Discount Calculator"),
    "price-markup-calculator": _calc([
        {"name": "cost", "label": "Product Cost ($)", "type": "number", "required": True, "min": 0, "step": 0.01},
        {"name": "markup_percent", "label": "Markup (%)", "type": "number", "required": True, "min": 0, "step": 1},
    ], ["profit-margin-calculator", "discount-calculator", "fba-profit-calculator", "unit-economics-calculator"], "Price Markup Calculator"),
    "unit-economics-calculator": _calc([
        {"name": "sale_price", "label": "Sale Price ($)", "type": "number", "required": True, "min": 0, "step": 0.01},
        {"name": "total_cost", "label": "Total Cost per Unit ($)", "type": "number", "required": True, "min": 0, "step": 0.01},
        {"name": "monthly_units", "label": "Monthly Units Sold", "type": "number", "required": True, "min": 0, "step": 1},
    ], ["profit-margin-calculator", "break-even-calculator", "fba-profit-calculator", "roi-calculator"], "Unit Economics Calculator"),
}
