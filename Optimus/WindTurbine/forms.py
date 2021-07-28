from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(label='Airfoilname', max_length=100)
