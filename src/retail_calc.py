"""
Retail Checkout & Pricing Calculation Engine
Core business logic for order totals, promotional discounts, and sales tax.
"""

def calculate_subtotal(items: list) -> float:
    """Calculate the gross subtotal of cart items."""
    if not items:
        return 0.0
    return round(sum(item["price"] * item["quantity"] for item in items), 2)

def apply_discount(subtotal: float, promo_code: str = "") -> float:
    """Apply promotional coupons to the subtotal."""
    clean_code = (promo_code or "").strip().upper()
    discount_rate = 0.0
    
    if clean_code == "WELCOME10":
        discount_rate = 0.10
    elif clean_code == "VIP20":
        discount_rate = 0.20
    elif clean_code == "FLASH50":
        discount_rate = 0.50
        
    discount_amount = round(subtotal * discount_rate, 2)
    return round(subtotal - discount_amount, 2)

def calculate_sales_tax(taxable_amount: float, state: str = "TX") -> float:
    """Calculate sales tax by US state code."""
    tax_rates = {
        "TX": 0.0825,
        "CA": 0.0925,
        "NY": 0.08875,
        "IL": 0.0875,
        "FL": 0.0600
    }
    rate = tax_rates.get(state.upper(), 0.05)  # default 5%
    return round(taxable_amount * rate, 2)

def calculate_final_total(items: list, promo_code: str = "", state: str = "TX") -> dict:
    """Generate complete itemized financial invoice."""
    subtotal = calculate_subtotal(items)
    discounted_subtotal = apply_discount(subtotal, promo_code)
    discount_savings = round(subtotal - discounted_subtotal, 2)
    tax = calculate_sales_tax(discounted_subtotal, state)
    final_total = round(discounted_subtotal + tax, 2)
    
    return {
        "subtotal": subtotal,
        "discount_savings": discount_savings,
        "taxable_amount": discounted_subtotal,
        "sales_tax": tax,
        "final_total": final_total,
        "state": state.upper()
    }
