from django.contrib import admin
from .models import VisaCountry


# Register your models here.


class VisaCountryAdmin(admin.ModelAdmin):
    list_filter = [
        "country",
    ]
    list_display = ["country", "created", "lastupdated_by", "last_updated_on"]
    search_fields = ["country"]
    list_per_page = 10


admin.site.register(VisaCountry, VisaCountryAdmin)
