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


class VisaCategoryForm(forms.ModelForm):
    class Meta:
        model = VisaCategory
        fields = "__all__"
        widgets = {
            "visa_country_id": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),
            "category": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Category Name",
                }
            ),
            "subcategory": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "SubCategory Name",
                }
            ),
        }


class DocumentCategoryForm(forms.ModelForm):
    class Meta:
        model = DocumentCategory
        fields = "__all__"
        widgets = {
            "Document_category": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Document Category",
                }
            )
        }


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = "__all__"
        widgets = {
            "document_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Document Name",
                }
            ),
            "document_category": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),
        }


class CaseCategoryDocumentForm(forms.ModelForm):
    class Meta:
        model = CaseCategoryDocument
        fields = ["country", "category", "document"]

        widgets = {
            "country": forms.Select(attrs={"class": "form-control"}),
            "category": forms.Select(attrs={"class": "form-control"}),
            # 'subcategory': forms.Select(attrs={'class': 'form-control'}),
            "document": forms.CheckboxSelectMultiple(),
        }

        document = forms.ModelMultipleChoiceField(
            queryset=Document.objects.all(),
            required=False,
        )


class BranchForm(forms.ModelForm):
    class Meta:
        model = Branch
        fields = ["branch_name", "branch_source"]
        widgets = {
            "branch_name": forms.TextInput(attrs={"class": "form-control"}),
            "branch_source": forms.Select(attrs={"class": "form-control"}),
        }


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ["group_name", "group_member"]
        widgets = {
            "group_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter Group Name"}
            ),
        }

    group_member = forms.ModelMultipleChoiceField(
        queryset=CustomUser.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )


class CompanyCourierDetailsForm(forms.ModelForm):
    class Meta:
        model = CourierAddress
        fields = [
            "company_name",
            "address",
            "landmark",
            "city",
            "state",
            "zipcode",
            "docker_no",
            "courier_no",
            "status",
        ]

        widgets = {
            "company_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter Company Name"}
            ),
            "address": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter Address"}
            ),
            "landmark": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter Landmark"}
            ),
            "city": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter City"}
            ),
            "state": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter State"}
            ),
            "zipcode": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "Enter Zipcode"}
            ),
            "docker_no": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter Docker No"}
            ),
            "courier_no": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter Number"}
            ),
            "status": forms.Select(attrs={"class": "form-control"}),
        }


class ReceiverDetailsForm(forms.ModelForm):
    class Meta:
        model = CourierAddress
        fields = ["receiver_no", "sender_no", "receiver_address", "sender_address"]
        widgets = {
            "sender_no": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter Number"}
            ),
            "receiver_no": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter Number"}
            ),
            "receiver_address": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter Address"}
            ),
            "sender_address": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter Address"}
            ),
        }
