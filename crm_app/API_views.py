from rest_framework import viewsets
from .models import Booking, FrontWebsiteEnquiry, VisaCountry, VisaCategory, Package
from .serializers import (
    BookingSerializer,
    FrontWebsiteSerializer,
    VisaCategorySerializer,
    VisaCountrySerializer,
    ProductSerializer,
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
