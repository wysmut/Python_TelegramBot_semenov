from django.test import TestCase
from .models import Order

class OrderModelTest(TestCase):
    def test_create_order(self):
        order = Order.objects.create(description="Test Order", amount=100.00)
        self.assertEqual(order.description, "Test Order")
        self.assertEqual(order.amount, 100.00)
