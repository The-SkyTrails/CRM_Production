from django import forms
from django.core.validators import RegexValidator
from .models import *


class Step1Form(forms.Form):
    name = forms.CharField(max_length=100)


class Step2Form(forms.Form):
    email = forms.EmailField()


class Step3Form(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput)


class VisaCountryForm(forms.ModelForm):
    class Meta:
        model = VisaCountry
        fields = "__all__"
        widgets = {
            "country": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Country",
                }
            )
        }

        def clean_country_name(self):
            country_name = self.cleaned_data.get("country")
            existing_country = VisaCountry.objects.filter(country__iexact=country_name)

            if existing_country.exists():
                raise forms.ValidationError("This country already exists.")

            return country_name
