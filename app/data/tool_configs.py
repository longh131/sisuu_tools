"""
Tool page configurations — per docs/05 单工具页面规范.md
Each MVP tool has: fields, button_text, how_it_works, faqs, related_slugs
"""

TOOL_CONFIGS: dict[str, dict] = {
    "amazon-fee-calculator": {
        "tool_type": "calculator",
        "button_text": "Calculate",
        "how_it_works": [
            {"step": 1, "title": "Enter Product Details", "description": "Input your sale price, category and fulfillment method."},
            {"step": 2, "title": "Click Calculate", "description": "Our calculator instantly computes all Amazon fees."},
            {"step": 3, "title": "View Results", "description": "See referral fee, FBA fee and your net profit breakdown."},
        ],
        "fields": [
            {"name": "sale_price", "label": "Sale Price ($)", "type": "number", "placeholder": "29.99", "required": True, "min": 0, "step": 0.01},
            {"name": "category", "label": "Product Category", "type": "select", "required": True,
             "options": [
                 {"value": "general", "label": "General (15%)"},
                 {"value": "electronics", "label": "Electronics (8%)"},
                 {"value": "clothing", "label": "Clothing (17%)"},
                 {"value": "beauty", "label": "Beauty (8%)"},
                 {"value": "home", "label": "Home & Kitchen (15%)"},
             ]},
            {"name": "fulfillment", "label": "Fulfillment Method", "type": "select", "required": True,
             "options": [
                 {"value": "fba", "label": "FBA (Fulfillment by Amazon)"},
                 {"value": "fbm", "label": "FBM (Fulfilled by Merchant)"},
             ]},
            {"name": "item_weight", "label": "Item Weight (lbs)", "type": "number", "placeholder": "1.0", "required": False, "min": 0, "step": 0.1},
        ],
        "faqs": [
            {"question": "What is Amazon Fee Calculator?", "answer": "It calculates Amazon referral fees and FBA fulfillment fees based on your product price, category and fulfillment method."},
            {"question": "How accurate is this calculator?", "answer": "Our calculator uses standard Amazon fee rates. Actual fees may vary slightly based on your seller account and promotions."},
            {"question": "Is this tool free?", "answer": "Yes, the Amazon Fee Calculator is completely free with no registration required."},
            {"question": "Do I need to register?", "answer": "No registration is needed. Use the calculator instantly on any device."},
            {"question": "How often is fee data updated?", "answer": "We update fee rates when Amazon announces changes to their fee structure."},
        ],
        "related_slugs": ["fba-profit-calculator", "vat-calculator", "shipping-calculator", "product-description-generator"],
    },
    "fba-profit-calculator": {
        "tool_type": "calculator",
        "button_text": "Calculate",
        "how_it_works": [
            {"step": 1, "title": "Enter Cost Data", "description": "Input sale price, product cost, and all associated fees."},
            {"step": 2, "title": "Click Calculate", "description": "The calculator computes your net profit and margin."},
            {"step": 3, "title": "Analyze Results", "description": "Review profit margin, ROI and per-unit profit breakdown."},
        ],
        "fields": [
            {"name": "sale_price", "label": "Sale Price ($)", "type": "number", "placeholder": "39.99", "required": True, "min": 0, "step": 0.01},
            {"name": "product_cost", "label": "Product Cost ($)", "type": "number", "placeholder": "10.00", "required": True, "min": 0, "step": 0.01},
            {"name": "amazon_fees", "label": "Amazon Fees ($)", "type": "number", "placeholder": "8.00", "required": True, "min": 0, "step": 0.01},
            {"name": "shipping_cost", "label": "Shipping to Amazon ($)", "type": "number", "placeholder": "1.50", "required": False, "min": 0, "step": 0.01},
            {"name": "other_costs", "label": "Other Costs ($)", "type": "number", "placeholder": "0.50", "required": False, "min": 0, "step": 0.01},
        ],
        "faqs": [
            {"question": "What is FBA Profit Calculator?", "answer": "It calculates your net profit and profit margin after all Amazon FBA costs including product cost, fees and shipping."},
            {"question": "What is a good profit margin for Amazon?", "answer": "Most successful Amazon sellers aim for a 20-30% profit margin after all fees and costs."},
            {"question": "Is this calculator free?", "answer": "Yes, completely free with no account required."},
            {"question": "Can I include advertising costs?", "answer": "Use the Other Costs field to include PPC advertising or any additional expenses."},
            {"question": "How do I improve my profit margin?", "answer": "Reduce product costs, optimize packaging for lower FBA fees, and improve your listing conversion rate."},
        ],
        "related_slugs": ["amazon-fee-calculator", "vat-calculator", "shipping-calculator", "negative-review-reply"],
    },
    "vat-calculator": {
        "tool_type": "calculator",
        "button_text": "Calculate",
        "how_it_works": [
            {"step": 1, "title": "Enter Amount", "description": "Input the net or gross amount and select VAT rate."},
            {"step": 2, "title": "Click Calculate", "description": "Instantly compute VAT amount and total."},
            {"step": 3, "title": "View Breakdown", "description": "See net price, VAT amount and gross total."},
        ],
        "fields": [
            {"name": "amount", "label": "Amount ($)", "type": "number", "placeholder": "100.00", "required": True, "min": 0, "step": 0.01},
            {"name": "vat_rate", "label": "VAT Rate (%)", "type": "select", "required": True,
             "options": [
                 {"value": "20", "label": "UK Standard (20%)"},
                 {"value": "19", "label": "Germany (19%)"},
                 {"value": "21", "label": "Netherlands (21%)"},
                 {"value": "23", "label": "Ireland (23%)"},
                 {"value": "5", "label": "UK Reduced (5%)"},
                 {"value": "0", "label": "Zero Rate (0%)"},
             ]},
            {"name": "calc_type", "label": "Calculation Type", "type": "select", "required": True,
             "options": [
                 {"value": "add", "label": "Add VAT to net price"},
                 {"value": "extract", "label": "Extract VAT from gross price"},
             ]},
        ],
        "faqs": [
            {"question": "What is VAT Calculator?", "answer": "It calculates Value Added Tax for UK and EU eCommerce sales at various standard rates."},
            {"question": "Which VAT rates are supported?", "answer": "We support UK (20%, 5%), Germany (19%), Netherlands (21%), Ireland (23%) and zero-rated goods."},
            {"question": "Is this tool free?", "answer": "Yes, the VAT Calculator is free with no registration required."},
            {"question": "Do I need to register for VAT?", "answer": "UK sellers must register when annual turnover exceeds £90,000. EU thresholds vary by country."},
            {"question": "Can I use this for Amazon sales?", "answer": "Yes, use this calculator for any eCommerce sales where VAT applies."},
        ],
        "related_slugs": ["amazon-fee-calculator", "fba-profit-calculator", "shipping-calculator", "seller-guides"],
    },
    "shipping-calculator": {
        "tool_type": "calculator",
        "button_text": "Calculate",
        "how_it_works": [
            {"step": 1, "title": "Enter Package Details", "description": "Input weight, dimensions and destination zone."},
            {"step": 2, "title": "Click Calculate", "description": "Get estimated shipping costs instantly."},
            {"step": 3, "title": "Compare Options", "description": "View estimated costs for different shipping methods."},
        ],
        "fields": [
            {"name": "weight", "label": "Package Weight (lbs)", "type": "number", "placeholder": "2.0", "required": True, "min": 0.1, "step": 0.1},
            {"name": "destination", "label": "Destination Zone", "type": "select", "required": True,
             "options": [
                 {"value": "domestic", "label": "Domestic (US)"},
                 {"value": "canada", "label": "Canada"},
                 {"value": "uk", "label": "United Kingdom"},
                 {"value": "eu", "label": "European Union"},
                 {"value": "international", "label": "International"},
             ]},
            {"name": "service", "label": "Shipping Service", "type": "select", "required": True,
             "options": [
                 {"value": "standard", "label": "Standard (5-7 days)"},
                 {"value": "expedited", "label": "Expedited (2-3 days)"},
                 {"value": "express", "label": "Express (1-2 days)"},
             ]},
        ],
        "faqs": [
            {"question": "What is Shipping Calculator?", "answer": "It estimates shipping costs based on package weight, destination and service level."},
            {"question": "How accurate are shipping estimates?", "answer": "Estimates are based on standard carrier rate tables. Actual costs may vary by carrier and surcharges."},
            {"question": "Is this tool free?", "answer": "Yes, completely free with no registration required."},
            {"question": "Which carriers are supported?", "answer": "Estimates are based on standard USPS, UPS and FedEx rate structures for common package sizes."},
            {"question": "Can I use this for FBA inbound shipping?", "answer": "Yes, use this to estimate costs for shipping inventory to Amazon fulfillment centers."},
        ],
        "related_slugs": ["amazon-fee-calculator", "fba-profit-calculator", "vat-calculator", "seller-checklists"],
    },
    "negative-review-reply": {
        "tool_type": "ai",
        "button_text": "Generate",
        "how_it_works": [
            {"step": 1, "title": "Paste the Review", "description": "Copy and paste the negative customer review."},
            {"step": 2, "title": "Add Context", "description": "Optionally describe your product and the issue."},
            {"step": 3, "title": "Generate Reply", "description": "AI creates a professional, empathetic response."},
        ],
        "fields": [
            {"name": "review_text", "label": "Customer Review", "type": "textarea", "placeholder": "Paste the negative review here...", "required": True, "rows": 4},
            {"name": "product_name", "label": "Product Name", "type": "text", "placeholder": "e.g. Wireless Bluetooth Headphones", "required": False},
            {"name": "tone", "label": "Response Tone", "type": "select", "required": True,
             "options": [
                 {"value": "professional", "label": "Professional"},
                 {"value": "empathetic", "label": "Empathetic"},
                 {"value": "apologetic", "label": "Apologetic"},
             ]},
        ],
        "faqs": [
            {"question": "What is Review Reply Generator?", "answer": "An AI tool that generates professional responses to negative customer reviews on Amazon, eBay and other platforms."},
            {"question": "Is the AI reply ready to post?", "answer": "AI replies should always be reviewed and personalized before posting. They provide a strong starting point."},
            {"question": "Is this tool free?", "answer": "Yes, with free daily usage limits. No registration required for basic use."},
            {"question": "Which platforms does it support?", "answer": "Works for Amazon, eBay, Etsy, Shopify and any platform where you receive customer reviews."},
            {"question": "Can I edit the generated reply?", "answer": "Yes, the result is fully editable. Copy it and customize before posting."},
        ],
        "related_slugs": ["product-description-generator", "refund-reply-generator", "buyer-message-generator", "amazon-fee-calculator"],
    },
    "product-description-generator": {
        "tool_type": "ai",
        "button_text": "Generate",
        "how_it_works": [
            {"step": 1, "title": "Describe Your Product", "description": "Enter product name, features and target platform."},
            {"step": 2, "title": "Click Generate", "description": "AI creates an SEO-optimized product description."},
            {"step": 3, "title": "Copy & Use", "description": "Copy the description and paste into your listing."},
        ],
        "fields": [
            {"name": "product_name", "label": "Product Name", "type": "text", "placeholder": "e.g. Stainless Steel Water Bottle 32oz", "required": True},
            {"name": "features", "label": "Key Features", "type": "textarea", "placeholder": "List main features, materials, dimensions...", "required": True, "rows": 4},
            {"name": "platform", "label": "Target Platform", "type": "select", "required": True,
             "options": [
                 {"value": "amazon", "label": "Amazon"},
                 {"value": "ebay", "label": "eBay"},
                 {"value": "shopify", "label": "Shopify"},
                 {"value": "etsy", "label": "Etsy"},
             ]},
            {"name": "tone", "label": "Writing Tone", "type": "select", "required": True,
             "options": [
                 {"value": "professional", "label": "Professional"},
                 {"value": "persuasive", "label": "Persuasive"},
                 {"value": "friendly", "label": "Friendly"},
             ]},
        ],
        "faqs": [
            {"question": "What is Product Description Generator?", "answer": "An AI tool that creates SEO-optimized product descriptions for Amazon, eBay, Shopify and Etsy listings."},
            {"question": "Are descriptions SEO-optimized?", "answer": "Yes, descriptions include relevant keywords and are formatted for marketplace search algorithms."},
            {"question": "Is this tool free?", "answer": "Yes, with free daily usage. No registration required for basic use."},
            {"question": "Can I use descriptions on multiple platforms?", "answer": "Select your target platform for optimized formatting. You can adapt descriptions for other platforms."},
            {"question": "Should I edit AI descriptions?", "answer": "Always review and add specific product details. AI descriptions are a strong starting point, not a final copy."},
        ],
        "related_slugs": ["negative-review-reply", "refund-reply-generator", "amazon-fee-calculator", "fba-profit-calculator"],
    },
}

# Merge commercial-phase configs
from app.data.ai_tool_configs import AI_TOOL_CONFIGS  # noqa: E402
from app.data.marketplace_calc_configs import MARKETPLACE_CALC_CONFIGS  # noqa: E402

TOOL_CONFIGS.update(AI_TOOL_CONFIGS)
TOOL_CONFIGS.update(MARKETPLACE_CALC_CONFIGS)


def get_tool_config(slug: str) -> dict | None:
    """Return tool page config by slug."""
    return TOOL_CONFIGS.get(slug)


def get_default_config(tool: dict) -> dict:
    """Return a minimal config for tools without full MVP implementation."""
    return {
        "tool_type": "info",
        "button_text": "Learn More",
        "how_it_works": [
            {"step": 1, "title": "Browse Resource", "description": "Explore the information and resources available."},
            {"step": 2, "title": "Apply to Your Business", "description": "Use the insights for your eCommerce operations."},
            {"step": 3, "title": "Stay Updated", "description": "Check back for the latest updates and additions."},
        ],
        "fields": [],
        "faqs": [
            {"question": f"What is {tool['name']}?", "answer": tool.get("description", "")},
            {"question": "Is this resource free?", "answer": "Yes, all resources on Seller Toolkit are free to access."},
            {"question": "Do I need to register?", "answer": "No registration is required."},
            {"question": "How often is content updated?", "answer": "We regularly update our tools and resources."},
            {"question": "Can I suggest improvements?", "answer": "Contact us through our Contact page with suggestions."},
        ],
        "related_slugs": [],
    }
