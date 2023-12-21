from django.urls import path, include

from .AdminViews import *

urlpatterns = [
    path("Dashboard/", admin_dashboard, name="admin_dashboard"),
    path("AddVisaCountry/", add_visacountry, name="add_visacountry"),
    path("VisaCountry/update/", visacountryupdate_view, name="visacountryupdate_view"),
    path("import/Country", import_country, name="importcountry"),
    path(
        "VisaCountry/Delete/<int:id>", delete_visa_country, name="delete_visa_country"
    ),
    path("AddVisaCategory/", add_visacategory, name="add_visacategory"),
    path("VisaCategory/Edit/", visacategoryupdate_view, name="visacategoryupdate_view"),
    path("deletecategory/<int:id>/", delete_category, name="delete_category"),
    path("AddDocumentCategory/", add_documentcategory, name="add_documentcategory"),
    path(
        "DocumentCategory/Edit/",
        documentcategoryupdate_view,
        name="documentcategoryupdate_view",
    ),
    path(
        "deletedocumentcategory/<int:id>/",
        delete_documentcategory,
        name="delete_documentcategory",
    ),
    path("AddDocument/", add_document, name="add_document"),
    path("Document/Edit/", documentupdate_view, name="documentupdate_view"),
    path("deletedocument/<int:id>/", delete_document, name="delete_document"),
    path(
        "AddCaseCategoryDocument/",
        CaseCategoryDocumentCreateView.as_view(),
        name="add_CaseCategoryDocument",
    ),
    path(
        "CaseCategoryDocumentList/",
        CaseCategoryDocumentListView.as_view(),
        name="CaseCategoryDocument_list",
    ),
    path(
        "CaseCategoryDocumentEdit/<int:pk>",
        editCaseCategoryDocument.as_view(),
        name="editCaseCategoryDocument",
    ),
    path(
        "casecategorydocument/delete/<int:id>/",
        delete_casecategorydocument,
        name="delete_casecategorydocument",
    ),
    path("Addbranch/", add_branch, name="add_branch"),
    path("Branch/Edit/", branchupdate_view, name="branchupdate_view"),
    path("deletebranch/<int:id>/", delete_branch, name="delete_branch"),
    path("import/Branch", import_branch, name="import_branch"),
    path("create_group/", CreateGroupView.as_view(), name="create_group"),
    path("GroupList/", GroupListView.as_view(), name="Group_list"),
    path("GroupEdit/<int:pk>", editGroup.as_view(), name="editgroup"),
    path("group/delete/<int:id>/", delete_group, name="delete_group"),
    path("personal_details/", PersonalDetailsView.as_view(), name="personal_details"),
    path("receiver_details/", ReceiverDetailsView.as_view(), name="receiver_details"),
    path(
        "ViewCourierAddress/", viewcourieraddress_list, name="viewcourieraddress_list"
    ),
    path(
        "update_company_details/<int:id>/",
        UpdateCompanyDetailsView.as_view(),
        name="update_company_details",
    ),
    path(
        "update_receiver_details/<int:id>/",
        UpdateReceiverDetailsView.as_view(),
        name="update_receiver_details",
    ),
    path(
        "courierdetails/delete/<int:id>/",
        delete_courierdetails,
        name="delete_courierdetails",
    ),
    path("emp_personal_details/", add_employee, name="emp_personal_details"),
    path("emp_list/", all_employee.as_view(), name="emp_list"),
    path("Employe/Update/<int:pk>", employee_update, name="employee_update"),
    path("Employe/Update/Save", employee_update_save, name="employee_update_save"),
    path("Employee/delete/<int:id>/", delete_employee, name="delete_employee"),
    
    path("add_agent/", add_agent, name="add_agent"),
    path("agent_list/", all_agent.as_view(), name="agent_list"),
    path('AllOutSourceAgent/',all_outsource_agent.as_view(),name="all_outsource_agent"),
    
]
