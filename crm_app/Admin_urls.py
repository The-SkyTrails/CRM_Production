from django.urls import path, include

from .AdminViews import *

urlpatterns = [
    path("AddVisaCountry/", add_visacountry, name="add_visacountry"),
    path(
        "VisaCountry/update/",
        visacountryupdate_view,
        name="visacountryupdate_view",
    ),
    path(
        "VisaCountry/Delete/<int:id>", delete_visa_country, name="delete_visa_country"
    ),
    path("import/Country", import_country, name="importcountry"),
]
