from django import forms

from apps.collector import models


class PlaceForm(forms.ModelForm):
    """Form for place."""

    class Meta:
        model = models.Place
        fields = (
            "name",
            "description",
        )
