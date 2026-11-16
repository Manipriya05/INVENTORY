from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from inventory.models import StockMovement
from products.models import Category, Product
from .models import Sale, SaleItem


class SaleWorkflowTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='staff', password='test-password', is_staff=True
        )
        self.client.force_login(self.user)
        self.category = Category.objects.create(name='Office')
        self.product = Product.objects.create(
            name='Notebook',
            product_code='NOTE-1',
            category=self.category,
            purchase_price=Decimal('5.00'),
            selling_price=Decimal('10.00'),
            quantity=10,
        )

    def sale_data(self, first_quantity, second_quantity, second_product=None):
        data = {
            'customer': '',
            'gst': '2.00',
            'discount': '1.00',
            'form-TOTAL_FORMS': '2',
            'form-INITIAL_FORMS': '0',
            'form-MIN_NUM_FORMS': '1',
            'form-MAX_NUM_FORMS': '1000',
            'form-0-product': str(self.product.pk),
            'form-0-quantity': str(first_quantity),
            'form-0-price': '9.99',
            'form-1-product': str((second_product or self.product).pk),
            'form-1-quantity': str(second_quantity),
            'form-1-price': '10.00',
        }
        if second_quantity == 0:
            data.update({
                'form-1-product': '',
                'form-1-quantity': '',
                'form-1-price': '',
            })
        return data

    def test_duplicate_product_lines_are_aggregated_and_invoice_totals_are_correct(self):
        response = self.client.post(
            reverse('add_sale'), self.sale_data(2, 3)
        )

        self.assertRedirects(response, reverse('sale_list'))
        self.product.refresh_from_db()
        self.assertEqual(self.product.quantity, 5)
        self.assertEqual(Sale.objects.count(), 1)
        self.assertEqual(SaleItem.objects.count(), 2)
        self.assertEqual(StockMovement.objects.filter(movement_type='OUT').count(), 2)

        sale = Sale.objects.get()
        self.assertTrue(sale.invoice_number.startswith('INV-'))
        self.assertEqual(len(sale.invoice_number), 45)
        self.assertEqual(sale.subtotal, Decimal('49.98'))
        self.assertEqual(sale.grand_total, Decimal('50.98'))
        self.assertEqual(sale.items.first().line_total, Decimal('19.98'))

        invoice = self.client.get(reverse('invoice_detail', args=[sale.pk]))
        self.assertContains(invoice, '50.98')
        self.assertContains(invoice, '19.98')

    def test_multiple_products_can_be_sold_and_invoice_numbers_are_unique(self):
        second_product = Product.objects.create(
            name='Pencil',
            product_code='PEN-2',
            category=self.category,
            purchase_price=Decimal('2.00'),
            selling_price=Decimal('4.00'),
            quantity=5,
        )
        response = self.client.post(
            reverse('add_sale'),
            self.sale_data(2, 1, second_product=second_product),
        )

        self.assertRedirects(response, reverse('sale_list'))
        self.product.refresh_from_db()
        second_product.refresh_from_db()
        self.assertEqual(self.product.quantity, 8)
        self.assertEqual(second_product.quantity, 4)
        first_invoice = Sale.objects.get().invoice_number

        response = self.client.post(
            reverse('add_sale'),
            self.sale_data(1, 1, second_product=second_product),
        )
        self.assertRedirects(response, reverse('sale_list'))
        invoice_numbers = list(Sale.objects.values_list('invoice_number', flat=True))
        self.assertEqual(len(invoice_numbers), 2)
        self.assertEqual(len(set(invoice_numbers)), 2)
        self.assertIn(first_invoice, invoice_numbers)

    def test_combined_duplicate_lines_cannot_oversell(self):
        response = self.client.post(
            reverse('add_sale'), self.sale_data(6, 5)
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Insufficient stock')
        self.product.refresh_from_db()
        self.assertEqual(self.product.quantity, 10)
        self.assertFalse(Sale.objects.exists())
        self.assertFalse(StockMovement.objects.exists())

    def test_discount_cannot_exceed_invoice_amount(self):
        data = self.sale_data(1, 0)
        data['discount'] = '100.00'
        response = self.client.post(reverse('add_sale'), data)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Discount cannot exceed')
        self.assertFalse(Sale.objects.exists())

    def test_sale_form_exposes_add_line_control(self):
        response = self.client.get(reverse('add_sale'))

        self.assertContains(response, 'Add another product')
        self.assertContains(response, 'sale-item-template')

    def test_product_with_invoice_history_cannot_be_deleted(self):
        sale = Sale.objects.create(invoice_number='INV-HISTORY')
        SaleItem.objects.create(
            sale=sale,
            product=self.product,
            quantity=1,
            price=Decimal('10.00'),
        )

        response = self.client.post(
            reverse('delete_product', args=[self.product.pk])
        )

        self.assertRedirects(response, reverse('product_list'))
        self.assertTrue(Product.objects.filter(pk=self.product.pk).exists())
        self.assertTrue(SaleItem.objects.filter(sale=sale).exists())
