from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models.deletion import ProtectedError
from .models import Supplier
from .forms import SupplierForm
from django.db.models import Q
from accounts.decorators import staff_required


# View all suppliers
@staff_required
def supplier_list(request):
    query = request.GET.get('q', '')
    suppliers = Supplier.objects.all()
    if query:
        suppliers = suppliers.filter(
            Q(name__icontains=query) |
            Q(phone__icontains=query) |
            Q(email__icontains=query)
        )
    return render(request, 'suppliers/supplier_list.html', {
        'suppliers': suppliers,
        'query': query
    })
# Add supplier
@staff_required
def add_supplier(request):
    if request.method == 'POST':
        form = SupplierForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Supplier was added successfully.')
            return redirect('supplier_list')
    else:
        form = SupplierForm()

    return render(request, 'suppliers/add_supplier.html', {
        'form': form
    })
# Edit supplier
@staff_required
def edit_supplier(request, id):
    supplier = get_object_or_404(Supplier, id=id)

    if request.method == 'POST':
        form = SupplierForm(request.POST, instance=supplier)

        if form.is_valid():
            form.save()
            messages.success(request, 'Supplier was updated successfully.')
            return redirect('supplier_list')
    else:
        form = SupplierForm(instance=supplier)

    return render(request, 'suppliers/edit_supplier.html', {
        'form': form
    })
    
# Delete supplier
@staff_required
def delete_supplier(request, id):
    supplier = get_object_or_404(Supplier, id=id)

    if request.method == 'POST':
        try:
            supplier.delete()
        except ProtectedError:
            messages.error(
                request,
                'This supplier has purchase history and cannot be deleted.',
            )
        else:
            messages.success(request, 'Supplier was deleted successfully.')
        return redirect('supplier_list')

    return render(request, 'suppliers/delete_supplier.html', {
        'supplier': supplier
    })