"""
Integration & End-to-End API Tests for FastAPI Retail Engine
Tested automatically in GitHub Actions CI/CD pipeline.
"""
import unittest
import sys
from pathlib import Path
from fastapi.testclient import TestClient

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.main import app

class TestRetailAPI(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)

    def test_health_check_endpoint(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "healthy")
        self.assertEqual(data["service"], "retail-pricing-engine")

    def test_catalog_endpoint(self):
        response = self.client.get("/api/v1/catalog")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertGreaterEqual(data["count"], 4)
        skus = [p["sku"] for p in data["products"]]
        self.assertIn("SKU-HDPH-01", skus)

    def test_promo_code_validation_valid(self):
        response = self.client.post("/api/v1/promos/validate", json={"promo_code": "VIP20"})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["is_valid"])
        self.assertEqual(data["discount_percentage"], 20.0)

    def test_promo_code_validation_invalid(self):
        response = self.client.post("/api/v1/promos/validate", json={"promo_code": "FAKE100"})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertFalse(data["is_valid"])

    def test_checkout_calculation_standard(self):
        payload = {
            "items": [
                {"sku": "SKU-HDPH-01", "name": "Headphones", "price": 100.0, "quantity": 1},
                {"sku": "SKU-CHRG-02", "name": "Charger", "price": 50.0, "quantity": 1}
            ],
            "promo_code": "WELCOME10",
            "state": "TX"
        }
        response = self.client.post("/api/v1/checkout", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["subtotal"], 150.0)
        self.assertEqual(data["promo_savings"], 15.0)
        self.assertEqual(data["taxable_amount"], 135.0)
        # Tax in TX (8.25% of 135) = 11.14
        self.assertEqual(data["sales_tax"], 11.14)
        self.assertEqual(data["final_total"], 146.14)

    def test_checkout_bulk_volume_discount(self):
        payload = {
            "items": [
                {"sku": "SKU-CABLE-01", "name": "USB Cable", "price": 10.0, "quantity": 10}
            ],
            "promo_code": "",
            "state": "FL"
        }
        response = self.client.post("/api/v1/checkout", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["subtotal"], 100.0)
        # 15% bulk discount = 15.00
        self.assertEqual(data["bulk_savings"], 15.0)
        self.assertEqual(data["taxable_amount"], 85.0)
        # Tax in FL (6% of 85) = 5.10
        self.assertEqual(data["sales_tax"], 5.10)
        self.assertEqual(data["final_total"], 90.10)

    def test_checkout_empty_cart_error(self):
        response = self.client.post("/api/v1/checkout", json={"items": [], "state": "TX"})
        self.assertEqual(response.status_code, 400)

if __name__ == "__main__":
    unittest.main()
