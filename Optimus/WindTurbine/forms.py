from django import forms
from .models import Blade

class BladeForm(forms.ModelForm):
    class Meta:
        model = Blade
        fields = ["name", "length", "weight"]
