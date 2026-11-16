from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models.deletion import ProtectedError
from django.db.models import Q
from .models import Product, Category
from .forms import ProductForm, CategoryForm
from accounts.decorators import staff_required


@staff_required
def category_list(request):
    query = request.GET.get('q', '')
    categories = Category.objects.all()
    if query:
        categories = categories.filter(name__icontains=query)
    return render(request, 'products/category_list.html', {
        'categories': categories,
        'query': query,
    })


@staff_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category was added successfully.')
            return redirect('category_list')
    else:
        form = CategoryForm()

    return render(request, 'products/add_category.html', {
        'form': form,
    })


@staff_required
def edit_category(request, id):
    category = get_object_or_404(Category, id=id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category was updated successfully.')
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)

    return render(request, 'products/edit_category.html', {
        'form': form,
        'category': category,
    })


@staff_required
def delete_category(request, id):
    category = get_object_or_404(Category, id=id)
    if request.method == 'POST':
        if category.product_set.exists():
            messages.error(request, 'This category is being used by products and cannot be deleted.')
            return redirect('category_list')
        category.delete()
        messages.success(request, 'Category was deleted successfully.')
        return redirect('category_list')

    return render(request, 'products/delete_category.html', {
        'category': category,
    })


# View all products
@staff_required
def product_list(request):
    query = request.GET.get('q', '')
    products = Product.objects.all()
    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(product_code__icontains=query) |
            Q(category__name__icontains=query)
        )
    return render(request, 'products/product_list.html', {
        'products': products,
        'query': query
    })
# Add new product
@staff_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Product was added successfully.')
            return redirect('product_list')
    else:
        form = ProductForm()

    return render(request, 'products/add_product.html', {
        'form': form
    })


# Edit product
@staff_required
def edit_product(request, id):
    product = get_object_or_404(Product, id=id)

    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)

        if form.is_valid():
            form.save()
            messages.success(request, 'Product was updated successfully.')
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)

    return render(request, 'products/edit_product.html', {
        'form': form
    })


# Delete product
@staff_required
def delete_product(request, id):
    product = get_object_or_404(Product, id=id)

    if request.method == 'POST':
        try:
            product.delete()
        except ProtectedError:
            messages.error(
                request,
                'This product has purchase or sales history and cannot be deleted.',
            )
        else:
            messages.success(request, 'Product was deleted successfully.')
        return redirect('product_list')

    return render(request, 'products/delete_product.html', {
        'product': product
    })