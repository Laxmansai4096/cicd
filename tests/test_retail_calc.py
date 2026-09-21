"""
Automated Unit Tests for Retail Calculation Engine
Executed in GitHub Actions CI/CD Pipeline on every push & pull request.
"""
import unittest
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.retail_calc import (
    calculate_subtotal,
    apply_discount,
    apply_bulk_discount,
    calculate_sales_tax,
    calculate_final_total
)

class TestRetailCalculator(unittest.TestCase):
    
    def setUp(self):
        self.sample_items = [
            {"sku": "SKU-001", "name": "Wireless Headphones", "price": 100.00, "quantity": 1},
            {"sku": "SKU-002", "name": "USB-C Cable", "price": 20.00, "quantity": 2}
        ]
        self.bulk_items = [
            {"sku": "SKU-003", "name": "Keycaps Set", "price": 10.00, "quantity": 10}
        ]

    def test_subtotal_calculation(self):
        # 100*1 + 20*2 = 140.00
        subtotal = calculate_subtotal(self.sample_items)
        self.assertEqual(subtotal, 140.00)

    def test_empty_cart_subtotal(self):
        self.assertEqual(calculate_subtotal([]), 0.0)

    def test_promo_discount_vip20(self):
        # 100 - 20% = 80.00
        discounted = apply_discount(100.00, "VIP20")
        self.assertEqual(discounted, 80.00)

    def test_invalid_promo_code_no_discount(self):
        discounted = apply_discount(100.00, "INVALID_CODE")
        self.assertEqual(discounted, 100.00)

    def test_bulk_volume_discount_applied(self):
        # 10 items * $10.00 = $100.00 -> 15% bulk discount = $85.00
        net, savings = apply_bulk_discount(self.bulk_items, 100.00)
        self.assertEqual(net, 85.00)
        self.assertEqual(savings, 15.00)

    def test_sales_tax_tx(self):
        # 100 * 0.0825 = 8.25
        tax = calculate_sales_tax(100.00, "TX")
        self.assertEqual(tax, 8.25)

    def test_full_checkout_flow(self):
        result = calculate_final_total(self.sample_items, promo_code="WELCOME10", state="TX")
        # Subtotal: 140.00
        # WELCOME10 (-10% = -14.00) -> 126.00
        # Tax in TX: 126.00 * 0.0825 = 10.40
        # Total: 126.00 + 10.40 = 136.40
        self.assertEqual(result["subtotal"], 140.00)
        self.assertEqual(result["promo_savings"], 14.00)
        self.assertEqual(result["sales_tax"], 10.40)
        self.assertEqual(result["final_total"], 136.40)

if __name__ == "__main__":
    unittest.main()
