from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Customer
from .forms import CustomerForm
from django.shortcuts import get_object_or_404
from django.db.models import Q
from accounts.decorators import staff_required


@staff_required
def customer_list(request):
    query = request.GET.get('q', '')
    customers = Customer.objects.all()
    if query:
        customers = customers.filter(
            Q(name__icontains=query) |
            Q(phone__icontains=query) |
            Q(email__icontains=query)
        )
    return render(request, 'customers/customer_list.html', {
        'customers': customers,
        'query': query
    })
@staff_required
def add_customer(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Customer was added successfully.')
            return redirect('customer_list')
    else:
        form = CustomerForm()
    return render(request, 'customers/add_customer.html', {
        'form': form
    })
@staff_required
def edit_customer(request, id):
    customer = get_object_or_404(Customer, id=id)

    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)

        if form.is_valid():
            form.save()
            messages.success(request, 'Customer was updated successfully.')
            return redirect('customer_list')

    else:
        form = CustomerForm(instance=customer)

    return render(request, 'customers/edit_customer.html', {
        'form': form
    })
@staff_required
def delete_customer(request, id):
    customer = get_object_or_404(Customer, id=id)
    if request.method == 'POST':
        customer.delete()
        messages.success(request, 'Customer was deleted successfully.')
        return redirect('customer_list')

    return render(request, 'customers/delete_customer.html', {
        'customer': customer
    })