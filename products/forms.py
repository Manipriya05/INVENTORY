
from django import forms
from .models import Product, Category


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = [
            'name',
            'product_code',
            'category',
            'purchase_price',
            'selling_price',
            'quantity',
            'minimum_stock',
        ]
