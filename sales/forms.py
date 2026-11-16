from django import forms
from decimal import Decimal
from .models import Sale, SaleItem


class SaleForm(forms.ModelForm):
    gst = forms.DecimalField(
        max_digits=10, decimal_places=2, min_value=0, initial=Decimal('0.00')
    )
    discount = forms.DecimalField(
        max_digits=10, decimal_places=2, min_value=0, initial=Decimal('0.00')
    )

    class Meta:
        model = Sale
        fields = ['customer', 'gst', 'discount']


class SaleItemForm(forms.ModelForm):
    quantity = forms.IntegerField(min_value=1)
    price = forms.DecimalField(max_digits=10, decimal_places=2, min_value=0.01)

    class Meta:
        model = SaleItem
        fields = ['product', 'quantity', 'price']