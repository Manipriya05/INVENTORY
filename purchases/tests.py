from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from inventory.models import StockMovement
from products.models import Category, Product
from suppliers.models import Supplier
from .models import Purchase, PurchaseItem


class PurchaseWorkflowTests(TestCase):
    def setUp(self):
        user = get_user_model().objects.create_user(
            username='staff', password='test-password', is_staff=True
        )
        self.client.force_login(user)
        self.supplier = Supplier.objects.create(
            name='Paper Co', phone='1234567890', address='Main Street'
        )
        category = Category.objects.create(name='Office')
        self.product = Product.objects.create(
            name='Paper',
            product_code='PAPER-1',
            category=category,
            purchase_price=Decimal('4.00'),
            selling_price=Decimal('8.00'),
            quantity=7,
        )

    def test_duplicate_product_lines_increment_stock_and_total_once(self):
        response = self.client.post(reverse('add_purchase'), {
            'supplier': str(self.supplier.pk),
            'form-TOTAL_FORMS': '2',
            'form-INITIAL_FORMS': '0',
            'form-MIN_NUM_FORMS': '1',
            'form-MAX_NUM_FORMS': '1000',
            'form-0-product': str(self.product.pk),
            'form-0-quantity': '2',
            'form-0-price': '4.50',
            'form-1-product': str(self.product.pk),
            'form-1-quantity': '3',
            'form-1-price': '5.00',
        })

        self.assertRedirects(response, reverse('purchase_list'))
        self.product.refresh_from_db()
        self.assertEqual(self.product.quantity, 12)
        self.assertEqual(Purchase.objects.count(), 1)
        self.assertEqual(PurchaseItem.objects.count(), 2)
        self.assertEqual(Purchase.objects.get().total_amount, Decimal('24.00'))
        self.assertEqual(StockMovement.objects.filter(movement_type='IN').count(), 2)

    def test_supplier_with_purchase_history_cannot_be_deleted(self):
        purchase = Purchase.objects.create(supplier=self.supplier)
        PurchaseItem.objects.create(
            purchase=purchase,
            product=self.product,
            quantity=1,
            price=Decimal('4.00'),
        )

        response = self.client.post(
            reverse('delete_supplier', args=[self.supplier.pk])
        )

        self.assertRedirects(response, reverse('supplier_list'))
        self.assertTrue(Supplier.objects.filter(pk=self.supplier.pk).exists())
        self.assertTrue(Purchase.objects.filter(pk=purchase.pk).exists())
