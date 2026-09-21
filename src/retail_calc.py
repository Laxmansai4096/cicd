"""
Retail Checkout & Pricing Calculation Engine
Core business logic for order totals, promotional discounts, and sales tax.
"""

VALID_PROMO_CODES = {
    "WELCOME10": 0.10,
    "VIP20": 0.20,
    "FLASH50": 0.50
}

def calculate_subtotal(items: list) -> float:
    """Calculate the gross subtotal of cart items."""
    if not items:
        return 0.0
    return round(sum(item["price"] * item["quantity"] for item in items), 2)

def apply_discount(subtotal: float, promo_code: str = "") -> float:
    """Apply promotional coupons to the subtotal."""
    clean_code = (promo_code or "").strip().upper()
    discount_rate = VALID_PROMO_CODES.get(clean_code, 0.0)
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

def apply_bulk_discount(items: list, subtotal: float) -> tuple:
    """Apply automatic volume discount (15%) when ordering 10 or more total items."""
    total_qty = sum(item.get("quantity", 0) for item in items)
    if total_qty >= 10:
        discount = round(subtotal * 0.15, 2)
        return round(subtotal - discount, 2), discount
    return subtotal, 0.0

def calculate_final_total(items: list, promo_code: str = "", state: str = "TX") -> dict:
    """Generate complete itemized financial invoice with promo codes and bulk tiers."""
    subtotal = calculate_subtotal(items)
    
    # 1. Apply bulk tier discount first
    post_bulk_subtotal, bulk_savings = apply_bulk_discount(items, subtotal)
    
    # 2. Apply promotional coupon discount
    discounted_subtotal = apply_discount(post_bulk_subtotal, promo_code)
    promo_savings = round(post_bulk_subtotal - discounted_subtotal, 2)
    total_savings = round(bulk_savings + promo_savings, 2)
    
    # 3. Calculate tax and grand total
    tax = calculate_sales_tax(discounted_subtotal, state)
    final_total = round(discounted_subtotal + tax, 2)
    
    return {
        "subtotal": subtotal,
        "bulk_savings": bulk_savings,
        "promo_savings": promo_savings,
        "total_savings": total_savings,
        "taxable_amount": discounted_subtotal,
        "sales_tax": tax,
        "final_total": final_total,
        "state": state.upper()
    }
