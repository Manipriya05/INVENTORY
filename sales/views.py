
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import transaction
from django.db.models import F
from django.forms import formset_factory
from django.utils import timezone
from django.shortcuts import get_object_or_404
from decimal import Decimal
import uuid

from .models import Sale, SaleItem
from .forms import SaleForm, SaleItemForm
from products.models import Product
from inventory.models import StockMovement
from accounts.decorators import staff_required


class StockUnavailable(Exception):
    pass


@staff_required
def sale_list(request):
    sales = Sale.objects.select_related(
        'customer'
    ).all().order_by('-id')

    return render(request, 'sales/sale_list.html', {
        'sales': sales
    })


@staff_required
def add_sale(request):
    SaleItemFormSet = formset_factory(
        SaleItemForm, extra=1, min_num=1, validate_min=True
    )

    if request.method == 'POST':
        sale_form = SaleForm(request.POST)
        item_formset = SaleItemFormSet(request.POST)

        if sale_form.is_valid() and item_formset.is_valid():

            items = [form.cleaned_data for form in item_formset if form.cleaned_data]

            if not items:
                item_formset.forms[0].add_error(
                    None, 'Add at least one product.'
                )

            else:
                quantities = {}
                for item in items:
                    product = item['product']
                    quantities[product.pk] = quantities.get(product.pk, 0) + item['quantity']

                subtotal = sum(
                    (item['quantity'] * item['price'] for item in items),
                    Decimal('0.00'),
                )
                gst = sale_form.cleaned_data['gst']
                discount = sale_form.cleaned_data['discount']
                if discount > subtotal + gst:
                    sale_form.add_error(
                        'discount', 'Discount cannot exceed the subtotal plus GST.'
                    )
                else:
                    try:
                        with transaction.atomic():
                            products = {
                                product.pk: product
                                for product in Product.objects.select_for_update().filter(
                                    pk__in=quantities
                                )
                            }
                            for product_id, quantity in quantities.items():
                                product = products.get(product_id)
                                if product is None:
                                    raise StockUnavailable(
                                        'A selected product no longer exists. '
                                        'Reload the form and try again.'
                                    )
                                if quantity > product.quantity:
                                    raise StockUnavailable(
                                        f'Insufficient stock for {product.name}. '
                                        f'Available: {product.quantity}'
                                    )

                            sale = sale_form.save(commit=False)
                            sale.invoice_number = (
                                f'INV-{timezone.now():%Y%m%d}-'
                                f'{uuid.uuid4().hex.upper()}'
                            )
                            sale.subtotal = subtotal
                            sale.grand_total = subtotal + gst - discount
                            sale.save()

                            for item in items:
                                product = item['product']
                                quantity = item['quantity']
                                SaleItem.objects.create(
                                    sale=sale,
                                    product=product,
                                    quantity=quantity,
                                    price=item['price'],
                                )
                                StockMovement.objects.create(
                                    product=product,
                                    movement_type='OUT',
                                    quantity=quantity,
                                    remarks=f'Sale {sale.invoice_number}',
                                )

                            for product_id, quantity in quantities.items():
                                updated = Product.objects.filter(
                                    pk=product_id, quantity__gte=quantity
                                ).update(quantity=F('quantity') - quantity)
                                if updated != 1:
                                    product = products[product_id]
                                    raise StockUnavailable(
                                        f'Stock changed while selling {product.name}. '
                                        'Please try again.'
                                    )
                    except StockUnavailable as error:
                        item_formset.forms[0].add_error(None, str(error))
                    else:
                        messages.success(
                            request,
                            f'Sale {sale.invoice_number} was saved successfully.',
                        )
                        return redirect('sale_list')

    else:
        sale_form = SaleForm()
        item_formset = SaleItemFormSet()

    return render(request, 'sales/add_sale.html', {
        'sale_form': sale_form,
        'item_formset': item_formset
    })


@staff_required
def invoice_detail(request, id):
    sale = get_object_or_404(
        Sale.objects.select_related('customer').prefetch_related(
            'items__product'
        ),
        id=id
    )

    return render(request, 'sales/invoice_detail.html', {
        'sale': sale
    })