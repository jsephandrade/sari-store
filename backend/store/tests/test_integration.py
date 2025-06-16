from decimal import Decimal
from django.db import connection
from rest_framework.test import APITestCase
from store.models import Product, Customer, UtangEntry, Sale

class StoreIntegrationTest(APITestCase):
    def test_full_flow(self):
        prod_data = {"name": "Coke", "sku": "P001", "price": "10.00", "stock": 50}
        r = self.client.post("/products/", prod_data, format="json")
        self.assertEqual(r.status_code, 201)
        pid = r.data["id"]
        with connection.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM store_product WHERE sku=%s", ["P001"])
            self.assertEqual(cur.fetchone()[0], 1)

        cust_res = self.client.post("/customers/", {"name": "Juan"}, format="json")
        self.assertEqual(cust_res.status_code, 201)
        cid = cust_res.data["id"]

        utang_res = self.client.post(
            "/utang/",
            {
                "customer": cid,
                "product": pid,
                "quantity": 2,
                "date_issued": "2023-01-01",
                "due_date": "2023-01-10",
            },
            format="json",
        )
        self.assertEqual(utang_res.status_code, 201)
        utang_id = utang_res.data["id"]
        utang = UtangEntry.objects.get(id=utang_id)
        self.assertEqual(utang.total_amount, Decimal("20.00"))

        pay_res = self.client.post(
            "/payments/", {"utang_entry": utang_id, "amount_paid": "20.00"}, format="json"
        )
        self.assertEqual(pay_res.status_code, 201)
        self.assertEqual(UtangEntry.objects.get(id=utang_id).status, "paid")

        sale_res = self.client.post(
            "/sales/",
            {
                "customer": cid,
                "payment_method": "cash",
                "items": [{"product": pid, "quantity": 1}],
            },
            format="json",
        )
        self.assertEqual(sale_res.status_code, 201)
        sale = Sale.objects.get(id=sale_res.data["id"])
        self.assertEqual(sale.total_amount, Decimal("10.00"))
        self.assertEqual(Product.objects.get(id=pid).stock, 49)

        summary = self.client.get("/summary/")
        self.assertEqual(summary.status_code, 200)
        self.assertIn("total_sales", summary.data)
