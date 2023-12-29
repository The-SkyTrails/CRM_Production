from django.contrib import admin
from .models import *


class VisaCountryAdmin(admin.ModelAdmin):
    list_filter = [
        "country",
    ]
    list_display = ["country", "created", "lastupdated_by", "last_updated_on"]
    search_fields = ["country"]
    list_per_page = 10


class CustomUserAdmin(admin.ModelAdmin):
    list_filter = [
        "email",
    ]
    list_display = ["email", "user_type"]
    search_fields = ["email"]
    list_per_page = 10


class AgentAdmin(admin.ModelAdmin):
    list_filter = [
        "users",
    ]
    list_display = ["users", "contact_no", "assign_employee"]
    search_fields = ["users"]
    list_per_page = 10


class OutsourceAdmin(admin.ModelAdmin):
    list_filter = [
        "users",
    ]
    list_display = ["users", "contact_no", "assign_employee"]
    search_fields = ["users"]
    list_per_page = 10


class EnquiryAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "enquiry_number",
        "assign_to_employee",
        "assign_to_sales_employee",
        "assign_to_documentation_employee",
        "assign_to_agent",
        "assign_to_visa_team_employee",
        "lead_status",
    ]


class EmployeeAdmin(admin.ModelAdmin):
    list_display = "users", "contact_no", "department"


class EnquiryAppointmentAdmin(admin.ModelAdmin):
    list_display = (
        "enquiry",
        "description",
        "date",
        "time",
        "status",
        "created_by",
        "created_date",
    )


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(VisaCountry, VisaCountryAdmin)
admin.site.register(VisaCategory)
admin.site.register(DocumentCategory)
admin.site.register(Document)
admin.site.register(CaseCategoryDocument)
admin.site.register(Branch)
admin.site.register(Agent, AgentAdmin)
admin.site.register(OutSourcingAgent, OutsourceAdmin)
admin.site.register(Group)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(AgentAgreement)
admin.site.register(Package)
admin.site.register(VisaSubcategory)
admin.site.register(Booking)
admin.site.register(FrontWebsiteEnquiry)
admin.site.register(Admin)
admin.site.register(Enquiry, EnquiryAdmin)
admin.site.register(DocumentFiles)
admin.site.register(Notes)
admin.site.register(AgentKyc)
admin.site.register(EnqAppointment, EnquiryAppointmentAdmin)
admin.site.register(Background_Information)
admin.site.register(Education_Summary)
admin.site.register(TestScore)
admin.site.register(Work_Experience)
