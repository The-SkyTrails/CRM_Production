from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin
from import_export import resources


class VisaCountryResource(resources.ModelResource):
    class Meta:
        model = VisaCountry
        fields = ("country", "created", "lastupdated_by", "last_updated_on")


class DocumentCategoryResource(ImportExportModelAdmin, admin.ModelAdmin):
    class Meta:
        model = DocumentCategory
        fields = (
            "Document_category",
            "lastupdated_by",
            "last_updated_on",
        )

    list_display = ["id", "Document_category", "lastupdated_by", "last_updated_on"]


class visaCategoryResource(ImportExportModelAdmin, admin.ModelAdmin):
    class Meta:
        model = VisaCategory

    list_display = [
        "id",
        "visa_country_id",
        "category",
        "subcategory",
        "lastupdated_by",
        "last_updated_on",
    ]


class DocumentResource(resources.ModelResource):
    class Meta:
        model = Document
        # fields = ("country", "created", "lastupdated_by", "last_updated_on")


class VisaCountryAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_filter = [
        "country",
    ]
    list_display = ["id", "country", "created", "lastupdated_by", "last_updated_on"]
    search_fields = ["country"]
    list_per_page = 10


class VisaCountryAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_filter = [
        "country",
    ]
    list_display = ["id", "country", "created", "lastupdated_by", "last_updated_on"]
    search_fields = ["country"]
    list_per_page = 10


class DocumentAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_filter = [
        "document_name",
    ]
    list_display = [
        "document_name",
        "document_category",
        "lastupdated_by",
        "last_updated_on",
    ]
    search_fields = ["document_name"]
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


class CustomUserResource(resources.ModelResource):
    class Meta:
        model = CustomUser


class EmployeeResource(resources.ModelResource):
    class Meta:
        model = Employee
        exclude = ("id",)  # Exclude fields if necessary


# class CustomUserAdmin(ImportExportModelAdmin, admin.ModelAdmin):
#     resource_class = CustomUserResource


class EmployeeAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = EmployeeResource
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


class FollowupAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "description",
        "follow_up_status",
        "priority",
        "calendar",
        "time",
        "remark",
        "enquiry",
        "created_by",
    )


class FaqAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "employee", "question", "answer", "last_updated_on"]


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(VisaCountry, VisaCountryAdmin)
admin.site.register(VisaCategory, visaCategoryResource)
admin.site.register(DocumentCategory, DocumentCategoryResource)
admin.site.register(Document, DocumentAdmin)
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
admin.site.register(FAQ, FaqAdmin)
admin.site.register(FollowUp, FollowupAdmin)
admin.site.register(ActivityLog)
admin.site.register(ChatGroup)
admin.site.register(ChatMessage)
admin.site.register(SuccessStory)
admin.site.register(News)
admin.site.register(Report)
