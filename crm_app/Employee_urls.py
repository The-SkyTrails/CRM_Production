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
    # ------------------------------------------- Agent ----------------------------------------
    path("add_agent/", emp_add_agent, name="emp_add_agent"),
    path("agent_list/", emp_all_agent.as_view(), name="emp_agent_list"),
    path("agent_Grid/", emp_allGrid_agent.as_view(), name="emp_agent_grid"),
    path("agent_delete/<int:id>/", employee_agent_delete, name="employee_agent_delete"),
    path("Agent/Details/<int:id>", emp_agent_details, name="emp_agent_details"),
    path(
        "Agent/Agreement/<int:id>",
        employee_agent_agreement,
        name="employee_agent_agreement",
    ),
    path(
        "Agent/Agreement/update/<int:id>/",
        employee_agent_agreement_update,
        name="employee_agent_agreement_update",
    ),
    path(
        "Agent/Agreement/Delete/<int:id>/",
        emp_agent_agreement_delete,
        name="emp_agent_agreement_delete",
    ),
    path("Agent/Kyc/<int:id>", emp_agent_kyc, name="emp_agent_kyc"),
    # ----------------------------- Out Source Agent -----------------------------
    path(
        "AllOutSourceAgent/",
        emp_all_outsource_agent.as_view(),
        name="emp_all_outsource_agent",
    ),
    path(
        "AllOutSourceAgentGrid/",
        emp_allGrid_outsource_agent.as_view(),
        name="emp_allgrid_outsource_agent",
    ),
    path(
        "Outsourceagent_delete/<int:id>/",
        emp_outstsourceagent_delete,
        name="emp_outstsourceagent_delete",
    ),
    path(
        "OutSourceAgent/Details/<int:id>",
        emp_outsourceagent_details,
        name="emp_outsourceagent_details",
    ),
    path(
        "OutSourceAgent/Agreement/<int:id>",
        emp_outsource_agent_agreement,
        name="emp_outsource_agent_agreement",
    ),
    path(
        "OutsourceAgent/Agreement/update/<int:id>/",
        emp_outsourceagent_agreement_update,
        name="emp_outsourceagent_agreement_update",
    ),
    path(
        "OutsourceAgent/Agreement/Delete/<int:id>/",
        emp_outsource_agent_agreement_delete,
        name="emp_outsource_agent_agreement_delete",
    ),
    path(
        "OutsourceAgent/Kyc/<int:id>",
        emp_outsource_agent_kyc,
        name="emp_outsource_agent_kyc",
    ),
    # ------------------------------------------------- Enrolled -------------------------
    path(
        "edit/Enrolled/Application/<int:id>",
        emp_edit_enrolled_application,
        name="emp_edit_enrolled_application",
    ),
    path("Educaion/Summary/<int:id>", emp_combined_view, name="emp_education_summary"),
    path("Product/<int:id>", emp_editproduct_details, name="emp_editproduct_details"),
    path(
        "enrolled_document/<int:id>/", emp_enrolleddocument, name="emp_enrolleddocument"
    ),
    path(
        "enrolledUploaddocument/",
        emp_enrolled_upload_document,
        name="emp_enrolled_upload_document",
    ),
    path(
        "Delete/enrolledUploadFile/<int:id>",
        emp_enrolled_delete_docfile,
        name="emp_enrolled_delete_docfile",
    ),
    # --------------------------------Follow Up-----------------------------
    path("Followup", followup, name="followup"),
    path("FollowupList/", emp_followup_list, name="emp_followup_list"),
    path("Followup/Delete/<int:id>", emp_followup_delete, name="emp_followup_delete"),
    path("followupupdate/", followup_update, name="followupupdate"),
    path("logout", employee_logout, name="employee_logout"),
    path("ChangePassword", ChangePassword, name="EmployeeChangePassword"),
    #  --------------------------------- FaQ -------------------------
    path("AddQueries/", emp_FAQCreateView.as_view(), name="emp_FAQCreateView"),
    path(
        "resolved-queries/",
        emp_ResolvedFAQListView,
        name="emp_ResolvedFAQListView",
    ),
    path(
        "pending-queries/",
        emp_PendingFAQListView,
        name="emp_PendingFAQListView",
    ),
    path("PackageList/", PackageListView.as_view(), name="Employee_Package_list"),
    path(
        "packages/<int:pk>/",
        PackageDetailView.as_view(),
        name="employee_package_detail",
    ),
]
