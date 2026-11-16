from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import transaction
from django.db.models import F
from django.forms import formset_factory
from decimal import Decimal
from .models import Purchase, PurchaseItem
from .forms import PurchaseForm, PurchaseItemForm
from products.models import Product
from inventory.models import StockMovement
from accounts.decorators import staff_required


@staff_required
def purchase_list(request):
    purchases = Purchase.objects.select_related(
        'supplier'
    ).all().order_by('-id')

    return render(request, 'purchases/purchase_list.html', {
        'purchases': purchases
    })


@staff_required
def add_purchase(request):

    PurchaseItemFormSet = formset_factory(
        PurchaseItemForm,
        extra=1,
        min_num=1,
        validate_min=True,
    )

    if request.method == 'POST':
        purchase_form = PurchaseForm(request.POST)
        item_formset = PurchaseItemFormSet(request.POST)

        if purchase_form.is_valid() and item_formset.is_valid():

            items = [
                form.cleaned_data
                for form in item_formset
                if form.cleaned_data
            ]

            if not items:
                item_formset.forms[0].add_error(
                    None, 'Add at least one product.'
                )
            else:
                with transaction.atomic():

                    purchase = purchase_form.save()
                    total = Decimal('0.00')

                    for item in items:
                        product = item['product']
                        quantity = item['quantity']
                        price = item['price']

                        PurchaseItem.objects.create(
                            purchase=purchase,
                            product=product,
                            quantity=quantity,
                            price=price
                        )

                        Product.objects.filter(pk=product.pk).update(
                            quantity=F('quantity') + quantity
                        )
                        StockMovement.objects.create(
                            product=product,
                            movement_type='IN',
                            quantity=quantity,
                            remarks=f'Purchase {purchase.pk}',
                        )

                        total += quantity * price

                    purchase.total_amount = total
                    purchase.save()

                messages.success(request, 'Purchase was saved successfully.')
                return redirect('purchase_list')

    else:
        purchase_form = PurchaseForm()
        item_formset = PurchaseItemFormSet()

    return render(request, 'purchases/add_purchase.html', {
        'purchase_form': purchase_form,
        'item_formset': item_formset
    })