import requests
from django.shortcuts import render
from rest_framework import viewsets
from .models import (
    Booking,
    FrontWebsiteEnquiry,
    VisaCountry,
    VisaCategory,
    Package,
    Enquiry,
)
from .serializers import (
    BookingSerializer,
    FrontWebsiteSerializer,
    VisaCategorySerializer,
    VisaCountrySerializer,
    ProductSerializer,
    EnquirySerializer,
)
from rest_framework.viewsets import ViewSet, ModelViewSet


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer


class FrontWebsite(ModelViewSet):
    queryset = FrontWebsiteEnquiry.objects.all()
    serializer_class = FrontWebsiteSerializer


class apiVisaCountry(ModelViewSet):
    queryset = VisaCountry.objects.all()
    serializer_class = VisaCountrySerializer


class apiVisaCategory(ModelViewSet):
    queryset = VisaCategory.objects.all()
    serializer_class = VisaCategorySerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Package.objects.filter(approval="True")
    serializer_class = ProductSerializer


class EnquiryViewSet(viewsets.ModelViewSet):
    # queryset = Enquiry.objects.all()
    serializer_class = EnquirySerializer

    def get_queryset(self):
        contact = self.request.query_params.get("contact")
        queryset = Enquiry.objects.filter(contact=contact)
        return queryset


def WebsitePackage(request):
    url = "https://back.theskytrails.com/skyTrails/packages/getAllcrm"
    response = requests.get(url)
    data = response.json()
    packages = data["data"]["pakage"]

    for package in packages:
        package["id"] = package.pop("_id")

    context = {"packages": packages}

    return render(request, "Admin/WebsitePackage/webPackage.html", context)


def EmployeeWebsitePackage(request):
    url = "https://back.theskytrails.com/skyTrails/packages/getAllcrm"
    response = requests.get(url)
    data = response.json()
    packages = data["data"]["pakage"]

    for package in packages:
        package["id"] = package.pop("_id")

    context = {"packages": packages}

    return render(request, "Employee/WebsitePackage/webPackage.html", context)


def AgentWebsitePackage(request):
    url = "https://back.theskytrails.com/skyTrails/packages/getAllcrm"
    response = requests.get(url)
    data = response.json()
    packages = data["data"]["pakage"]

    for package in packages:
        package["id"] = package.pop("_id")

    context = {"packages": packages}

    return render(request, "Agent/WebsitePackage/webPackage.html", context)
