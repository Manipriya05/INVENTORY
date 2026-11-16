from django.shortcuts import render, redirect
from accounts.decorators import staff_required
from django.contrib import messages
from django.db import transaction
from django.db.models import F
from products.models import Product
from .models import StockMovement
from .forms import StockMovementForm


@staff_required
def stock_movement_list(request):
    movements = StockMovement.objects.select_related('product').all().order_by('-date')

    return render(request, 'inventory/stock_movement_list.html', {
        'movements': movements
    })


@staff_required
def add_stock_movement(request):
    if request.method == 'POST':
        form = StockMovementForm(request.POST)
        if form.is_valid():
            movement = form.save(commit=False)
            with transaction.atomic():
                product = Product.objects.select_for_update().get(
                    pk=movement.product_id
                )
                if movement.movement_type == 'IN':
                    product.quantity += movement.quantity
                elif movement.movement_type == 'OUT':
                    if movement.quantity > product.quantity:
                        form.add_error('quantity', 'Insufficient stock available.')
                        return render(request, 'inventory/add_stock_movement.html', {
                            'form': form
                        })
                    product.quantity -= movement.quantity
                elif movement.movement_type == 'ADJUSTMENT':
                    product.quantity = movement.quantity
                product.save(update_fields=['quantity'])
                movement.save()
            messages.success(request, 'Stock movement was recorded successfully.')
            return redirect('stock_movement_list')

    else:
        form = StockMovementForm()

    return render(request, 'inventory/add_stock_movement.html', {
        'form': form
    })