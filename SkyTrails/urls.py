from django.contrib import admin
from django.urls import path, include
from crm_app import views


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("submit_form/", views.submit_form, name="submit_form"),
    path("multi-step-form/", views.multi_step_form, name="multi_step_form_step1"),
    path("Admin/", include("crm_app.Admin_urls")),
    path("Agent/", include("crm_app.Agent_urls")),
]
