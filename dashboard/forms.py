from django import forms


class ReportFilterForm(forms.Form):
    REPORT_CHOICES = (
        ('daily_sales', 'Daily sales'),
        ('monthly_sales', 'Monthly sales'),
        ('purchases', 'Purchases'),
        ('stock', 'Product stock'),
        ('low_stock', 'Low stock'),
    )

    report = forms.ChoiceField(choices=REPORT_CHOICES)
    start_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'}),
    )
    end_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'}),
    )

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        if start_date and end_date and start_date > end_date:
            self.add_error('end_date', 'End date must be on or after start date.')
        return cleaned_data
