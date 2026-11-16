from decimal import Decimal

from django.db.models import DecimalField, ExpressionWrapper, F, Sum, Count, Q
from django.shortcuts import render
from django.utils import timezone
from django.db.models.functions import TruncMonth

from products.models import Product, Category
from suppliers.models import Supplier
from customers.models import Customer
from sales.models import Sale
from purchases.models import Purchase
from accounts.decorators import staff_required
from .forms import ReportFilterForm


@staff_required
def dashboard(request):
    inventory_value = Product.objects.aggregate(
        value=Sum(
            ExpressionWrapper(
                F('quantity') * F('purchase_price'),
                output_field=DecimalField(max_digits=22, decimal_places=2),
            )
        )
    )['value'] or Decimal('0.00')
    context = {
        'total_products': Product.objects.count(),
        'total_suppliers': Supplier.objects.count(),
        'total_customers': Customer.objects.count(),
        'total_sales': Sale.objects.count(),
        'total_purchases': Purchase.objects.count(),
        'sales_amount': Sale.objects.aggregate(total=Sum('grand_total'))['total']
        or Decimal('0.00'),
        'purchase_amount': Purchase.objects.aggregate(
            total=Sum('total_amount')
        )['total'] or Decimal('0.00'),
        'inventory_value': inventory_value,
        'low_stock_count': Product.objects.filter(
            quantity__lte=F('minimum_stock')
        ).count(),
        'recent_sales': Sale.objects.select_related('customer').order_by(
            '-sale_date'
        )[:5],
        'recent_purchases': Purchase.objects.select_related('supplier').order_by(
            '-purchase_date', '-id'
        )[:5],
        'today': timezone.localdate(),
    }
    return render(request, 'dashboard/dashboard.html', context)


@staff_required
def mall_overview(request):
    products = Product.objects.select_related('category').annotate(
        stock_value=ExpressionWrapper(
            F('quantity') * F('purchase_price'),
            output_field=DecimalField(max_digits=22, decimal_places=2),
        )
    )
    category_summary = Category.objects.annotate(
        product_count=Count('product'),
        total_stock=Sum('product__quantity'),
        total_value=Sum(
            ExpressionWrapper(
                F('product__quantity') * F('product__purchase_price'),
                output_field=DecimalField(max_digits=22, decimal_places=2),
            )
        ),
        low_stock=Count('product', filter=Q(product__quantity__lte=F('product__minimum_stock'))),
    ).order_by('name')

    total_stock_units = products.aggregate(total=Sum('quantity'))['total'] or 0
    total_inventory_value = products.aggregate(value=Sum(
        ExpressionWrapper(
            F('quantity') * F('purchase_price'),
            output_field=DecimalField(max_digits=22, decimal_places=2),
        )
    ))['value'] or Decimal('0.00')
    low_stock_products = products.filter(quantity__lte=F('minimum_stock'))

    context = {
        'categories': category_summary,
        'products': products.order_by('category__name', 'name'),
        'total_categories': Category.objects.count(),
        'total_products': products.count(),
        'total_stock_units': total_stock_units,
        'total_inventory_value': total_inventory_value,
        'low_stock_products': low_stock_products[:8],
        'low_stock_count': low_stock_products.count(),
    }
    return render(request, 'dashboard/mall_overview.html', context)


@staff_required
def reports(request):
    today = timezone.localdate()
    initial = {
        'report': request.GET.get('report', 'daily_sales'),
        'start_date': today,
        'end_date': today,
    }
    if initial['report'] == 'monthly_sales':
        initial['start_date'] = today.replace(day=1)

    form = ReportFilterForm(request.GET if request.GET else initial, initial=initial)
    context = {'form': form, 'report_type': initial['report']}
    if form.is_valid():
        report_type = form.cleaned_data['report']
        start_date = form.cleaned_data['start_date'] or initial['start_date']
        end_date = form.cleaned_data['end_date'] or initial['end_date']
        if start_date > end_date:
            start_date, end_date = end_date, start_date

        sales = Sale.objects.filter(sale_date__date__range=(start_date, end_date))
        purchases = Purchase.objects.filter(
            purchase_date__range=(start_date, end_date)
        )
        context.update({
            'report_type': report_type,
            'start_date': start_date,
            'end_date': end_date,
            'sales_total': sales.aggregate(total=Sum('grand_total'))['total']
            or Decimal('0.00'),
            'purchases_total': purchases.aggregate(
                total=Sum('total_amount')
            )['total'] or Decimal('0.00'),
        })

        if report_type == 'daily_sales':
            context['sales'] = sales.select_related('customer').order_by(
                '-sale_date'
            )
        elif report_type == 'monthly_sales':
            context['sales_by_month'] = sales.annotate(
                report_month=TruncMonth('sale_date')
            ).values('report_month').annotate(
                total=Sum('grand_total')
            ).order_by('report_month')
        elif report_type == 'purchases':
            context['purchases'] = purchases.select_related('supplier').order_by(
                '-purchase_date', '-id'
            )
        else:
            products = Product.objects.select_related('category').annotate(
                stock_value=ExpressionWrapper(
                    F('quantity') * F('purchase_price'),
                    output_field=DecimalField(max_digits=22, decimal_places=2),
                )
            ).order_by('name')
            if report_type == 'low_stock':
                products = products.filter(quantity__lte=F('minimum_stock'))
            context['products'] = products

    return render(request, 'dashboard/reports.html', context)