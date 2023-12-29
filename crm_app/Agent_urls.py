from django.urls import path, include
from .AgentViews import *

urlpatterns = [
    path("Dashboard/", agent_dashboard.as_view(), name="agent_dashboard"),
    
    path("AddEnquiry/", Enquiry1View.as_view(), name="agent_enquiry_form1"),
    path("AddEnquiry2/", Enquiry2View.as_view(), name="agent_enquiry_form2"),
    path("AddEnquiry3/", Enquiry3View.as_view(), name="agent_enquiry_form3"),
    path("enquiry_form4/<int:id>/", agentdocument, name="agent_enquiry_form4"),
    path("Uploaddocument/", upload_document, name="agent_uploaddocument"),
    path("Delete/UploadFile/<int:id>", delete_docfile, name="agent_docfile"),
    # ------------------------------- LEADS ------------------------
    path("AllNewLeads", agent_new_leads_details, name="agent_new_leads_details"),
    path("AddNotes/", agent_add_notes, name="agent_add_notes"),
    path("Resend/<int:id>/", resend, name="resend"),
    
    path('edit/Enrolled/Application/<int:id>',edit_enrolled_application,name="agent_edit_enrolled_application"),
    path('Educaion/Summary/<int:id>',combined_view,name="agent_education_summary"),
    path('Test/Score/Delete/<int:id>',delete_test_score,name="agent_delete_test_score"),
    path('Product/<int:id>',editproduct_details,name="agent_edit_product_details"),
    path("enrolled_document/<int:id>/", enrolleddocument, name="agent_enrolled_document"),
    path("enrolledUploaddocument/", enrolled_upload_document, name="agent_enrolleduploaddocument"),
    path("Delete/enrolledUploadFile/<int:id>", enrolled_delete_docfile, name="agent_enrolleddocfile"),
    
    path("PackageList/", PackageListView.as_view(), name="Agent_Package_list"),
    path("packages/<int:pk>/", PackageDetailView.as_view(), name="Agent_package_detail"),
    
    path('logout', agent_logout,name="agent_logout"),
    
    path('ChangePassword',ChangePassword,name="AgentChangePassword"),
    
    path('AddQueries/', FAQCreateView.as_view(),name="Agent_addfaq"),
    path('resolved-queries/', ResolvedFAQListView.as_view(), name='resolved_queries'),
    path('pending-queries/', PendingFAQListView.as_view(), name='pending_queries'),
    
]
