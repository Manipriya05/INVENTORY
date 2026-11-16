from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from products.models import Category, Product
from sales.models import Sale
from sales.models import SaleItem
from customers.models import Customer
from inventory.models import StockMovement
from purchases.models import Purchase
from suppliers.models import Supplier


class DashboardAndReportTests(TestCase):
    def setUp(self):
        user = get_user_model().objects.create_user(
            username='staff', password='test-password', is_staff=True
        )
        self.client.force_login(user)
        Product.objects.all().delete()
        category = Category.objects.create(name='Office')
        Product.objects.create(
            name='Pen',
            product_code='PEN-1',
            category=category,
            purchase_price=Decimal('2.00'),
            selling_price=Decimal('5.00'),
            quantity=3,
            minimum_stock=5,
        )
        Sale.objects.create(
            invoice_number='INV-TEST-1',
            subtotal=Decimal('10.00'),
            gst=Decimal('1.00'),
            discount=Decimal('0.00'),
            grand_total=Decimal('11.00'),
        )

    def test_dashboard_uses_database_totals_and_recent_sales(self):
        response = self.client.get(reverse('dashboard'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['inventory_value'], Decimal('6.00'))
        self.assertEqual(response.context['sales_amount'], Decimal('11.00'))
        self.assertEqual(response.context['low_stock_count'], 1)
        self.assertContains(response, 'INV-TEST-1')

    def test_reports_support_date_filters(self):
        response = self.client.get(reverse('reports'), {
            'report': 'daily_sales',
            'start_date': '2000-01-01',
            'end_date': '2000-01-02',
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['sales_total'], Decimal('0.00'))
        self.assertContains(response, 'No sales in this period.')

    def test_each_report_type_renders(self):
        for report_type in (
            'daily_sales',
            'monthly_sales',
            'purchases',
            'stock',
            'low_stock',
        ):
            with self.subTest(report=report_type):
                response = self.client.get(reverse('reports'), {
                    'report': report_type,
                    'start_date': '2026-01-01',
                    'end_date': '2026-12-31',
                })
                self.assertEqual(response.status_code, 200)

    def test_staff_can_open_all_module_pages(self):
        product = Product.objects.get(product_code='PEN-1')
        customer = Customer.objects.create(name='Walk In', phone='1234567890')
        supplier = Supplier.objects.create(
            name='Paper Co', phone='1234567890', address='Main Street'
        )
        sale = Sale.objects.get(invoice_number='INV-TEST-1')
        SaleItem.objects.create(
            sale=sale, product=product, quantity=1, price=Decimal('5.00')
        )
        Purchase.objects.create(supplier=supplier)
        StockMovement.objects.create(
            product=product, movement_type='IN', quantity=1
        )

        pages = (
            ('dashboard', ()),
            ('reports', ()),
            ('product_list', ()),
            ('add_product', ()),
            ('edit_product', (product.pk,)),
            ('delete_product', (product.pk,)),
            ('supplier_list', ()),
            ('add_supplier', ()),
            ('edit_supplier', (supplier.pk,)),
            ('delete_supplier', (supplier.pk,)),
            ('customer_list', ()),
            ('add_customer', ()),
            ('edit_customer', (customer.pk,)),
            ('delete_customer', (customer.pk,)),
            ('stock_movement_list', ()),
            ('add_stock_movement', ()),
            ('purchase_list', ()),
            ('add_purchase', ()),
            ('sale_list', ()),
            ('add_sale', ()),
            ('invoice_detail', (sale.pk,)),
        )
        for route_name, args in pages:
            with self.subTest(route=route_name):
                response = self.client.get(reverse(route_name, args=args))
                self.assertEqual(response.status_code, 200)

# Create your tests here.
