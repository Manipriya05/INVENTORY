from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from products.models import Category, Product


class StockMovementTests(TestCase):
    def setUp(self):
        user = get_user_model().objects.create_user(
            username='staff', password='test-password', is_staff=True
        )
        self.client.force_login(user)
        category = Category.objects.create(name='Office')
        self.product = Product.objects.create(
            name='Pen',
            product_code='PEN-1',
            category=category,
            purchase_price=Decimal('2.00'),
            selling_price=Decimal('5.00'),
            quantity=4,
        )

    def test_adjustment_can_set_stock_to_zero(self):
        response = self.client.post(reverse('add_stock_movement'), {
            'product': str(self.product.pk),
            'movement_type': 'ADJUSTMENT',
            'quantity': '0',
            'remarks': 'Physical stock count',
        })

        self.assertRedirects(response, reverse('stock_movement_list'))
        self.product.refresh_from_db()
        self.assertEqual(self.product.quantity, 0)

    def test_stock_in_requires_positive_quantity(self):
        response = self.client.post(reverse('add_stock_movement'), {
            'product': str(self.product.pk),
            'movement_type': 'IN',
            'quantity': '0',
            'remarks': '',
        })

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'must be greater than zero')
        self.product.refresh_from_db()
        self.assertEqual(self.product.quantity, 4)
