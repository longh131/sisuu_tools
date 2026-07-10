"""VAT calculator — local computation."""


def calculate(data: dict) -> dict:
    """Calculate VAT amount from input data."""
    amount = float(data.get("amount", 0))
    vat_rate = float(data.get("vat_rate", 20))
    calc_type = data.get("calc_type", "add")

    if calc_type == "add":
        vat_amount = round(amount * vat_rate / 100, 2)
        gross_total = round(amount + vat_amount, 2)
        net_price = amount
    else:
        gross_total = amount
        net_price = round(amount / (1 + vat_rate / 100), 2)
        vat_amount = round(gross_total - net_price, 2)

    return {
        "net_price": net_price,
        "vat_amount": vat_amount,
        "gross_total": gross_total,
        "vat_rate": vat_rate,
        "calc_type": "Add VAT" if calc_type == "add" else "Extract VAT",
        "summary": (
            f"Net: ${net_price:.2f} | VAT ({vat_rate}%): ${vat_amount:.2f} | "
            f"Gross: ${gross_total:.2f}"
        ),
    }
