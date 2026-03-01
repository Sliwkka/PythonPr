from decimal import Decimal

from django import forms
from django.core.validators import MinValueValidator


class CarListForm(forms.Form):
    brand = forms.CharField(max_length=32, required=False)
    segment = forms.CharField(max_length=32, required=False)
    price = forms.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))],
                               required=False)
