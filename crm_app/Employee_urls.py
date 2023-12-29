from django.urls import path, include
from .EmployeeViews import *

urlpatterns = [
    path("Dashboard/", employee_dashboard.as_view(), name="employee_dashboard"),
    
    path("AddEnquiry/", emp_Enquiry1View.as_view(), name="emp_enquiry_form1"),
    path("AddEnquiry2/", emp_Enquiry2View.as_view(), name="emp_enquiry_form2"),
    path("AddEnquiry3/", emp_Enquiry3View.as_view(), name="emp_enquiry_form3"),
    path("enquiry_form4/<int:id>/", empdocument, name="emp_enquiry_form4"),
    path("Uploaddocument/", emp_upload_document, name="emp_upload_document"),
    path("Delete/UploadFile/<int:id>", emp_delete_docfile, name="emp_delete_docfile"),
    path("Lead/List/", employee_lead_list, name="employee_lead_list"),
    path("Lead/Grid/", employee_lead_grid, name="employee_lead_grid"),
    path("Lead/Details/", employee_lead_details, name="employee_lead_details"),
    path("Other/Details", employee_other_details, name="employee_other_details"),
    path(
        "Product/Selection/",
        employee_product_selection,
        name="employee_product_selection",
    ),
    path("Documents/", employee_lead_documents, name="employee_lead_documents"),
    path("Enrollled/Lead/", employee_enrolled_lead, name="employee_enrolled_lead"),
    path("Enrollled/Grid/", employee_enrolled_grid, name="employee_enrolled_grid"),
    # ------------------------------ Add lead staging --------------------------
    path("PreEnrolled/Save/<int:id>/", preenrolled_save, name="preenrolled_save"),
    path("Enrolled/Save/<int:id>/", enrolled_save, name="enrolled_save"),
    path("Enprocess/Save/<int:id>/", enprocess_save, name="enprocess_save"),
    path(
        "Ready_to_submit/Save/<int:id>/",
        ready_to_submit_save,
        name="ready_to_submit_save",
    ),
    path(
        "appointment_save/Save/<int:id>/",
        appointment_save,
        name="appointment_save",
    ),
    path(
        "ready_to_collection_save/Save/<int:id>/",
        ready_to_collection_save,
        name="ready_to_collection_save",
    ),
    path(
        "result_save/Save/<int:id>/",
        result_save,
        name="result_save",
    ),
    path(
        "delivery_Save/Save/<int:id>/",
        delivery_Save,
        name="delivery_Save",
    ),
    path("Reject/Save/<int:id>/", reject_save, name="reject_save"),
    path("Enq/Appointment/Save", enq_appointment_Save, name="enq_appointment_Save"),
    path(
        "Enq/Appointment/Done/<int:id>/",
        appointment_done,
        name="appointment_done",
    ),
    path("AddNotes/", emp_add_notes, name="emp_add_notes"),
    
    
    path('logout', employee_logout,name="employee_logout"),
    
    path('ChangePassword',ChangePassword,name="EmployeeChangePassword"),
]
