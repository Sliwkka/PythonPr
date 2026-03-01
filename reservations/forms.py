from decimal import Decimal

from django import forms
from django.core.validators import MinValueValidator

from reservations.models import Model

CarListSegmentChoices = {
    "": "-------"
}
CarListSegmentChoices.update(Model.SEGMENT_CHOICES)
"""
{
        "":"-------",
        "A": "budget",
        "B": "basic",
        "C": "compact",
        "D": "delux",
        "E": "executive",
}
"""


class CarListForm(forms.Form):
    brand = forms.ChoiceField(required=False)
    segment = forms.ChoiceField(choices=CarListSegmentChoices,
                                required=False)  # jesli mamy choices zdefiniowane w modelu
    price = forms.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))], required=False)
    start_date = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))
