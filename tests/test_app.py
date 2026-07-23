import unittest

from app import app


class QuickCartAppTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_products_api_contains_many_items(self):
        response = self.client.get("/api/products")
        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertGreaterEqual(len(payload["products"]), 20)
        self.assertIn("Essentials", payload["categories"])

    def test_order_endpoint_accepts_cart(self):
        response = self.client.post(
            "/api/order",
            json={
                "items": [{"id": 1, "quantity": 2}],
                "customer": {"name": "Ana", "phone": "9999999999", "address": "Block A"},
            },
        )
        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["order"]["items"][0]["quantity"], 2)


if __name__ == "__main__":
    unittest.main()
