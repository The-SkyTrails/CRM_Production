from django.contrib import admin
from .models import *

# Register your models here.


class VisaCountryAdmin(admin.ModelAdmin):
    list_filter = [
        "country",
    ]
    list_display = ["country", "created", "lastupdated_by", "last_updated_on"]
    search_fields = ["country"]
    list_per_page = 10


admin.site.register(VisaCountry, VisaCountryAdmin)
admin.site.register(VisaCategory)
admin.site.register(DocumentCategory)
admin.site.register(Document)
admin.site.register(CaseCategoryDocument)
admin.site.register(Branch)