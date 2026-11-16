from django import forms
from .models import Purchase, PurchaseItem


class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ['supplier']


class PurchaseItemForm(forms.ModelForm):
    quantity = forms.IntegerField(min_value=1)
    price = forms.DecimalField(max_digits=10, decimal_places=2, min_value=0.01)

    class Meta:
        model = PurchaseItem
        fields = ['product', 'quantity', 'price']