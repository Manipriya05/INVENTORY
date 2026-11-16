from django import forms
from .models import StockMovement


class StockMovementForm(forms.ModelForm):
    quantity = forms.IntegerField(min_value=0)

    class Meta:
        model = StockMovement
        fields = [
            'product',
            'movement_type',
            'quantity',
            'remarks'
        ]

    def clean(self):
        cleaned_data = super().clean()
        if (
            cleaned_data.get('quantity') == 0
            and cleaned_data.get('movement_type') != 'ADJUSTMENT'
        ):
            self.add_error('quantity', 'Stock in and stock out must be greater than zero.')
        return cleaned_data