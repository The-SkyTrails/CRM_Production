from django import forms
from django.core.validators import RegexValidator
from .models import *


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
        queryset=CustomUser.objects.exclude(user_type=1),
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


class PackageForm(forms.ModelForm):
    class Meta:
        model = Package
        fields = [
            "visa_country",
            "visa_category",
            "title",
            "description",
            "number_of_visa",
            "amount",
            "advance_amount",
            "file_charges",
            "package_expiry_date",
            "assign_to_group",
            "image",
        ]
        widgets = {
            "visa_country": forms.Select(attrs={"class": "form-control"}),
            "visa_category": forms.Select(attrs={"class": "form-control"}),
            "title": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter Title Name"}
            ),
            "description": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter Description"}
            ),
            "number_of_visa": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter Number of Visa"}
            ),
            "amount": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter Amount"}
            ),
            "advance_amount": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter Advance Amount"}
            ),
            "file_charges": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter File Charges"}
            ),
            "package_expiry_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter Package Expiry Date",
                    "type": "date",
                }
            ),
            "assign_to_group": forms.Select(attrs={"class": "form-control"}),
            "image": forms.FileInput(attrs={"class": "form-control"}),
        }


class VisasubCategoryForm(forms.ModelForm):
    class Meta:
        model = VisaSubcategory
        fields = [
            "country_id",
            "category_id",
            "subcategory_name",
            "estimate_amt",
            "cgst",
            "sgst",
        ]
        widgets = {
            "country_id": forms.Select(attrs={"class": "form-control"}),
            "category_id": forms.Select(attrs={"class": "form-control"}),
            "subcategory_name": forms.Select(attrs={"class": "form-control"}),
            "estimate_amt": forms.NumberInput(attrs={"class": "form-controls"}),
            "cgst": forms.NumberInput(attrs={"class": "form-controls"}),
            "sgst": forms.NumberInput(attrs={"class": "form-controls"}),
        }
        # labels = {'country_id': 'Country','category_id':'Category','subcategory_name':'Subcategory','estimate_amt':'Estimated Amount(INR)'}
        labels = {
            "country_id": "Country",
            "category_id": "Category",
            "subcategory_name": "Subcategory",
            "estimate_amt": "Estimated Amount (INR)",
            "cgst": "CGST (%)",
            "sgst": "SGST (%)",
        }


class EnquiryForm1(forms.ModelForm):
    class Meta:
        model = Enquiry
        fields = [
            "FirstName",
            "LastName",
            "email",
            "contact",
            "Dob",
            "Gender",
            "Country",
            "passport_no",
        ]

        widgets = {
            "email": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "Enter Email Id"}
            ),
            "contact": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter Contact No"}
            ),
            "FirstName": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter First Name"}
            ),
            "LastName": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter Last Name"}
            ),
            "Dob": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "Gender": forms.Select(attrs={"class": "form-control"}),
            "Country": forms.Select(attrs={"class": "form-control"}),
            "passport_no": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter Passport Number"}
            ),
        }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # Customize the Package field queryset if needed
            self.fields["Package"].queryset = Package.objects.all()


class EnquiryForm2(forms.ModelForm):
    class Meta:
        model = Enquiry
        fields = [
            "spouse_name",
            "spouse_no",
            "spouse_email",
            "spouse_passport",
            "spouse_dob",
        ]

        widgets = {
            "spouse_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter Spouse Name"}
            ),
            "spouse_no": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter Spouse Contact Number",
                }
            ),
            "spouse_email": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter Spouse Email"}
            ),
            "spouse_passport": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter Spouse Passport Number",
                }
            ),
            "spouse_dob": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                },
            ),
        }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # Customize the Package field queryset if needed
            self.fields["Package"].queryset = Package.objects.all()


class EnquiryForm3(forms.ModelForm):
    class Meta:
        model = Enquiry
        fields = [
            "Visa_country",
            "Visa_category",
            "Visa_subcategory",
            "Visa_type",
            "Package",
            "Source",
            "Reference",
        ]

        widgets = {
            "Visa_country": forms.Select(attrs={"class": "form-select"}),
            "Visa_category": forms.Select(attrs={"class": "form-select"}),
            "Visa_subcategory": forms.Select(attrs={"class": "form-select"}),
            "Visa_type": forms.Select(attrs={"class": "form-select"}),
            "Package": forms.Select(attrs={"class": "form-select"}),
            "Source": forms.Select(
                attrs={"class": "form-select", "placeholder": "Enter Source Name"}
            ),
            "Reference": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter Reference Name"}
            ),
        }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # Customize the Package field queryset if needed
            self.fields["Package"].queryset = Package.objects.all()


class FollowUpForm(forms.ModelForm):
    class Meta:
        model = FollowUp
        fields = [
            "title",
            "description",
            "follow_up_status",
            "priority",
            "calendar",
            "time",
            "remark",
        ]

        widgets = {
            "title": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter Title"}
            ),
            "description": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter Description"}
            ),
            "follow_up_status": forms.Select(attrs={"class": "form-select"}),
            "priority": forms.Select(attrs={"class": "form-select"}),
            "calendar": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter Date",
                    "type": "date",
                }
            ),
            "time": forms.TimeInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter Time",
                    "type": "time",
                }
            ),
            "remark": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter Remark"}
            ),
        }


class FAQForm(forms.ModelForm):
    class Meta:
        model = FAQ
        fields = ["question", "answer"]
        widgets = {
            "question": forms.Textarea(
                attrs={"class": "input-item", "placeholder": "Type your question here."}
            ),
            "answer": forms.Textarea(attrs={"class": "form-control"}),
        }


class ChatGroupForm(forms.ModelForm):
    class Meta:
        model = ChatGroup
        fields = ["group_name", "group_member"]
        widgets = {
            "group_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter Group Name"}
            ),
        }

    group_member = forms.ModelMultipleChoiceField(
        queryset=CustomUser.objects.exclude(user_type=1),
        widget=forms.CheckboxSelectMultiple,
    )
