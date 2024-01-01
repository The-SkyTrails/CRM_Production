from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import (
    CreateView,
    ListView,
    UpdateView,
    DetailView,
    TemplateView,
)
from .forms import *
from django.urls import reverse_lazy
from django.db.models import Prefetch
import requests
from .SMSAPI.whatsapp_api import send_whatsapp_message, send_sms_message
from django.core.mail import send_mail
from datetime import datetime
from django.utils import timezone

from django.contrib.auth import authenticate, logout, login as auth_login
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q


def employee_query_list(request):
    user = request.user
    dep = user.employee.department
    context = {"dep": dep}
    return render(request, "Employee/Queries/querieslist.html", context)


def employee_pending_query(request):
    user = request.user
    dep = user.employee.department
    context = {"dep": dep}
    return render(request, "Employee/Queries/pending_query.html", context)


def employee_followup_list(request):
    user = request.user
    dep = user.employee.department
    context = {"dep": dep}
    return render(request, "Employee/FollowUp/followup_list.html", context)


# ----------------------------------------------------------------


class employee_dashboard(LoginRequiredMixin, TemplateView):
    template_name = "Employee/Dashboard/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        agent_count = Agent.objects.filter(registerdby=self.request.user).count

        outsourceagent_count = OutSourcingAgent.objects.filter(
            registerdby=self.request.user
        ).count

        leadpending_count = Enquiry.objects.filter(
            lead_status="PreEnrolled", created_by=self.request.user
        ).count()

        leadcomplete_count = Enquiry.objects.filter(
            lead_status="Delivery", created_by=self.request.user
        ).count()

        leadaccept_count = Enquiry.objects.filter(
            Q(lead_status="Enrolled")
            | Q(lead_status="Inprocess")
            | Q(lead_status="Ready To Submit")
            | Q(lead_status="Appointment")
            | Q(lead_status="Ready To Collection")
            | Q(lead_status="Result")
            | Q(lead_status="Delivery"),
            created_by=self.request.user,
        ).count()

        lead_count = Enquiry.objects.filter(created_by=self.request.user).count()

        leadnew_count = Enquiry.objects.filter(
            lead_status="New Lead", created_by=self.request.user
        ).count()

        package = Package.objects.all().order_by("-last_updated_on")[:10]

        user = self.request.user
        if user.user_type == "4":
            agent = Agent.objects.get(users=user)
            context["agent"] = agent

        if user.user_type == "5":
            outagent = OutSourcingAgent.objects.get(users=user)
            context["agent"] = outagent

        dep = user.employee.department
        context["dep"] = dep

        context["leadcomplete_count"] = leadcomplete_count
        context["leadaccept_count"] = leadaccept_count
        context["leadpending_count"] = leadpending_count
        context["lead_count"] = lead_count
        context["leadnew_count"] = leadnew_count
        context["package"] = package
        context["agent_count"] = agent_count
        context["outsourceagent_count"] = outsourceagent_count

        return context


class emp_Enquiry1View(LoginRequiredMixin, CreateView):
    def get(self, request):
        form = EnquiryForm1()
        user = request.user
        dep = user.employee.department
        context = {"dep": dep, "form": form}
        return render(request, "Employee/Enquiry/lead1.html", context)

    def post(self, request):
        form = EnquiryForm1(request.POST)
        if form.is_valid():
            cleaned_data = {
                "FirstName": form.cleaned_data["FirstName"],
                "LastName": form.cleaned_data["LastName"],
                "email": form.cleaned_data["email"],
                "contact": form.cleaned_data["contact"],
                "Dob": form.cleaned_data["Dob"].strftime("%Y-%m-%d"),
                "Gender": form.cleaned_data["Gender"],
                "Country": form.cleaned_data["Country"],
                "passport_no": form.cleaned_data["passport_no"],
            }
            request.session["enquiry_form1"] = cleaned_data
            return redirect("emp_enquiry_form2")

        return render(
            request,
            "Admin/Enquiry/lead2.html",
            {"form": form},
        )


class emp_Enquiry2View(LoginRequiredMixin, CreateView):
    def get(self, request):
        form = EnquiryForm2()
        user = request.user
        dep = user.employee.department
        context = {"dep": dep, "form": form}
        return render(request, "Employee/Enquiry/lead2.html", context)

    def post(self, request):
        form = EnquiryForm2(request.POST)
        if form.is_valid():
            # Retrieve personal details from session
            enquiry_form1 = request.session.get("enquiry_form1", {})

            spouse_dob = form.cleaned_data.get("spouse_dob")
            cleaned_data = {
                "spouse_name": form.cleaned_data["spouse_name"],
                "spouse_no": form.cleaned_data["spouse_no"],
                "spouse_email": form.cleaned_data["spouse_email"],
                "spouse_passport": form.cleaned_data["spouse_passport"],
            }

            if spouse_dob:
                cleaned_data["spouse_dob"] = spouse_dob.strftime("%Y-%m-%d")

            # Merge personal details with receiver details
            merged_data = {**enquiry_form1, **cleaned_data}

            # Save the merged data to the session
            request.session["enquiry_form2"] = merged_data
            return redirect("emp_enquiry_form3")

        return render(
            request,
            "Employee/Enquiry/lead2.html",
            {"form": form},
        )


class emp_Enquiry3View(LoginRequiredMixin, CreateView):
    def get(self, request):
        form = EnquiryForm3()
        user = request.user
        dep = user.employee.department
        context = {"dep": dep, "form": form}
        return render(request, "Employee/Enquiry/lead3.html", context)

    def post(self, request):
        form1_data = request.session.get("enquiry_form1", {})
        form2_data = request.session.get("enquiry_form2", {})
        form3 = EnquiryForm3(request.POST)

        if form3.is_valid():
            user = request.user
            form3.instance.assign_to_employee = user.employee
            # Merge data from all three forms
            merged_data = {
                **form1_data,
                **form2_data,
                **form3.cleaned_data,
            }

            # Save the merged data to the database
            enquiry = Enquiry(**merged_data)
            user = self.request.user
            emp_dep = user.employee
            if emp_dep.department == "Presales/Assesment":
                enquiry.assign_to_employee = self.request.user.employee

            elif emp_dep.department == "Sales":
                lat_assigned_index = cache.get("lst_assigned_index") or 0
                presale_employees = get_presale_employee()
                if presale_employees.exists():
                    next_index = (lat_assigned_index + 1) % presale_employees.count()
                    enquiry.assign_to_employee = presale_employees[next_index]
                    enquiry.assign_to_sales_employee = self.request.user.employee

                    cache.set("lst_assigned_index", next_index)
            elif emp_dep.department == "Documentation":
                last_assigned_index = cache.get("last_assigned_index") or 0
                presale_employees = get_presale_employee()
                if presale_employees.exists():
                    next_index = (last_assigned_index + 1) % presale_employees.count()
                    enquiry.assign_to_employee = presale_employees[next_index]
                    enquiry.assign_to_documentation_employee = (
                        self.request.user.employee
                    )

                    cache.set("last_assigned_index", next_index)

            elif emp_dep.department == "Visa Team":
                last_assigned_index = cache.get("last_assigned_index") or 0
                presale_employees = get_presale_employee()
                if presale_employees.exists():
                    next_index = (last_assigned_index + 1) % presale_employees.count()
                    enquiry.assign_to_employee = presale_employees[next_index]
                    enquiry.assign_to_documentation_employee = (
                        self.request.user.employee
                    )

                    cache.set("last_assigned_index", next_index)
            enquiry.created_by = self.request.user
            enquiry.lead_status = "Active"
            enquiry.save()
            messages.success(request, "Enquiry Added successfully")

            # Clear session data after successful submission
            request.session.pop("enquiry_form1", None)
            request.session.pop("enquiry_form2", None)

            return redirect("emp_enquiry_form4", id=enquiry.id)

        return render(
            request,
            "Employee/Enquiry/lead3.html",
            {"form": form3},
        )

    def get_success_url(self):
        enquiry_id = self.object.id
        return reverse_lazy("emp_enquiry_form4", kwargs={"id": enquiry_id})


def get_presale_employee():
    return Employee.objects.filter(department="Presales/Assesment")


@login_required
def empdocument(request, id):
    enq = Enquiry.objects.get(id=id)
    document = Document.objects.all()
    user = request.user
    dep = user.employee.department

    doc_file = DocumentFiles.objects.filter(enquiry_id=enq)

    case_categories = CaseCategoryDocument.objects.filter(country=enq.Visa_country)

    documents_prefetch = Prefetch(
        "document",
        queryset=Document.objects.select_related("document_category", "lastupdated_by"),
    )

    case_categories = case_categories.prefetch_related(documents_prefetch)

    grouped_documents = {}

    for case_category in case_categories:
        for document in case_category.document.all():
            document_category = document.document_category
            testing = document.document_category.id

            if document_category not in grouped_documents:
                grouped_documents[document_category] = []

            grouped_documents[document_category].append(document)

    context = {
        "enq": enq,
        "grouped_documents": grouped_documents,
        "doc_file": doc_file,
        "dep": dep,
    }

    return render(request, "Employee/Enquiry/lead4.html", context)


@login_required
def emp_upload_document(request):
    if request.method == "POST":
        document_id = request.POST.get("document_id")
        enq_id = request.POST.get("enq_id")

        document = Document.objects.get(pk=document_id)
        document_file = request.FILES.get("document_file")
        enq = Enquiry.objects.get(id=enq_id)
        # Check if a DocumentFiles object with the same document exists
        try:
            doc = DocumentFiles.objects.filter(
                enquiry_id=enq_id, document_id=document
            ).first()
            if doc:
                doc.document_file = document_file
                doc.lastupdated_by = request.user
                doc.save()

                return redirect("enquiry_form4", id=enq_id)
            else:
                documest_files = DocumentFiles.objects.create(
                    document_file=document_file,
                    document_id=document,
                    enquiry_id=enq,
                    lastupdated_by=request.user,
                )
                documest_files.save()
                return redirect("emp_enquiry_form4", enq_id)

        except Exception as e:
            pass


@login_required
def emp_delete_docfile(request, id):
    doc_id = DocumentFiles.objects.get(id=id)
    enq_id = Enquiry.objects.get(id=doc_id.enquiry_id.id)
    enqq = enq_id.id

    doc_id.delete()
    return redirect("emp_enquiry_form4", enqq)


# -------------------------------------- Leads ------------------------------


@login_required
def employee_lead_list(request):
    user = request.user

    if user.is_authenticated:
        if user.user_type == "3":
            emp = user.employee
            dep = emp.department
            if dep == "Presales/Assesment":
                enq = Enquiry.objects.filter(
                    assign_to_employee=user.employee, created_by=user
                ).order_by("-id")
            elif dep == "Sales":
                enq = Enquiry.objects.filter(
                    assign_to_sales_employee=user.employee, created_by=user
                ).order_by("-id")
            elif dep == "Documentation":
                enq = Enquiry.objects.filter(
                    assign_to_documentation_employee=user.employee, created_by=user
                ).order_by("-id")
            elif dep == "Visa Team":
                enq = Enquiry.objects.filter(
                    assign_to_visa_team_employee=user.employee, created_by=user
                ).order_by("-id")
            else:
                enq = Enquiry.objects.filter(created_by=request.user)
            print("enquiryyyyy", enq)
            context = {"enq": enq, "user": user, "dep": dep}
    return render(request, "Employee/Enquiry/lead_list.html", context)


def employee_lead_grid(request):
    user = request.user

    if user.is_authenticated:
        if user.user_type == "3":
            emp = user.employee
            dep = emp.department
            if dep == "Presales/Assesment":
                enq = Enquiry.objects.filter(
                    assign_to_employee=user.employee, created_by=user
                ).order_by("-id")
            elif dep == "Sales":
                enq = Enquiry.objects.filter(
                    assign_to_sales_employee=user.employee, created_by=user
                ).order_by("-id")
            elif dep == "Documentation":
                enq = Enquiry.objects.filter(
                    assign_to_documentation_employee=user.employee, created_by=user
                ).order_by("-id")
            elif dep == "Visa Team":
                enq = Enquiry.objects.filter(
                    assign_to_visa_team_employee=user.employee, created_by=user
                ).order_by("-id")
            else:
                enq = None
            print("enquiryyyyy", enq)
            context = {"enq": enq, "user": user, "dep": dep}
    return render(request, "Employee/Enquiry/lead-grid.html", context)


def employee_enrolled_lead(request):
    user = request.user

    if user.is_authenticated:
        if user.user_type == "3":
            emp = user.employee
            dep = emp.department
            if dep == "Presales/Assesment":
                enq = Enquiry.objects.filter(
                    Q(lead_status="Enrolled")
                    | Q(lead_status="Inprocess")
                    | Q(lead_status="Ready To Submit")
                    | Q(lead_status="Appointment")
                    | Q(lead_status="Ready To Collection")
                    | Q(lead_status="Result")
                    | Q(lead_status="Delivery"),
                    assign_to_employee=user.employee,
                ).order_by("-id")
            elif dep == "Sales":
                enq = Enquiry.objects.filter(
                    Q(lead_status="Enrolled")
                    | Q(lead_status="Inprocess")
                    | Q(lead_status="Ready To Submit")
                    | Q(lead_status="Appointment")
                    | Q(lead_status="Ready To Collection")
                    | Q(lead_status="Result")
                    | Q(lead_status="Delivery"),
                    assign_to_sales_employee=user.employee,
                ).order_by("-id")
            elif dep == "Documentation":
                enq = Enquiry.objects.filter(
                    Q(lead_status="Enrolled")
                    | Q(lead_status="Inprocess")
                    | Q(lead_status="Ready To Submit")
                    | Q(lead_status="Appointment")
                    | Q(lead_status="Ready To Collection")
                    | Q(lead_status="Result")
                    | Q(lead_status="Delivery"),
                    assign_to_documentation_employee=user.employee,
                ).order_by("-id")
            elif dep == "Visa Team":
                enq = Enquiry.objects.filter(
                    Q(lead_status="Enrolled")
                    | Q(lead_status="Inprocess")
                    | Q(lead_status="Ready To Submit")
                    | Q(lead_status="Appointment")
                    | Q(lead_status="Ready To Collection")
                    | Q(lead_status="Result")
                    | Q(lead_status="Delivery"),
                    assign_to_visa_team_employee=user.employee,
                ).order_by("-id")
            else:
                enq = None

            context = {"enq": enq, "user": user, "dep": dep}

    return render(
        request, "Employee/Enquiry/Enrolled Enquiry/Enrolledleads.html", context
    )


def employee_enrolled_grid(request):
    user = request.user

    if user.is_authenticated:
        if user.user_type == "3":
            emp = user.employee
            dep = emp.department
            if dep == "Presales/Assesment":
                enq = Enquiry.objects.filter(
                    Q(lead_status="Enrolled")
                    | Q(lead_status="Inprocess")
                    | Q(lead_status="Ready To Submit")
                    | Q(lead_status="Appointment")
                    | Q(lead_status="Ready To Collection")
                    | Q(lead_status="Result")
                    | Q(lead_status="Delivery"),
                    assign_to_employee=user.employee,
                ).order_by("-id")
            elif dep == "Sales":
                enq = Enquiry.objects.filter(
                    Q(lead_status="Enrolled")
                    | Q(lead_status="Inprocess")
                    | Q(lead_status="Ready To Submit")
                    | Q(lead_status="Appointment")
                    | Q(lead_status="Ready To Collection")
                    | Q(lead_status="Result")
                    | Q(lead_status="Delivery"),
                    assign_to_sales_employee=user.employee,
                ).order_by("-id")
            elif dep == "Documentation":
                enq = Enquiry.objects.filter(
                    Q(lead_status="Enrolled")
                    | Q(lead_status="Inprocess")
                    | Q(lead_status="Ready To Submit")
                    | Q(lead_status="Appointment")
                    | Q(lead_status="Ready To Collection")
                    | Q(lead_status="Result")
                    | Q(lead_status="Delivery"),
                    assign_to_documentation_employee=user.employee,
                ).order_by("-id")
            elif dep == "Visa Team":
                enq = Enquiry.objects.filter(
                    Q(lead_status="Enrolled")
                    | Q(lead_status="Inprocess")
                    | Q(lead_status="Ready To Submit")
                    | Q(lead_status="Appointment")
                    | Q(lead_status="Ready To Collection")
                    | Q(lead_status="Result")
                    | Q(lead_status="Delivery"),
                    assign_to_visa_team_employee=user.employee,
                ).order_by("-id")
            else:
                enq = None

            context = {"enq": enq, "user": user, "dep": dep}
    return render(request, "Employee/Enquiry/enroll_lead-grid.html", context)


# --------------------------------------------------------------


def get_sale_employee():
    return Employee.objects.filter(department="Sales")


def get_documentation_team_employee():
    return Employee.objects.filter(department="Documentation")


def get_visa_team_employee():
    return Employee.objects.filter(department="Visa Team")


def preenrolled_save(request, id):
    enquiry = Enquiry.objects.get(id=id)
    agnt = enquiry.assign_to_agent
    sale_Emp = enquiry.assign_to_sales_employee
    doc_Emp = enquiry.assign_to_documentation_employee
    visa_Emp = enquiry.assign_to_visa_team_employee

    if agnt:
        agent_id = Agent.objects.get(id=agnt.id)
        sales_emp = agent_id.assign_employee

        enquiry.lead_status = "PreEnrolled"
        enquiry.assign_to_sales_employee = sales_emp
        enquiry.save()
        return redirect("employee_lead_list")

    if sale_Emp:
        enquiry.lead_status = "PreEnrolled"
        enquiry.save()
        return redirect("employee_lead_list")

    if doc_Emp:
        enquiry.lead_status = "PreEnrolled"
        enquiry.save()
        return redirect("employee_lead_list")
    if visa_Emp:
        print("vissaaa", visa_Emp)
        enquiry.lead_status = "PreEnrolled"
        enquiry.save()
        return redirect("employee_lead_list")

    else:
        last_assigned_index = cache.get("last_assigned_index") or 0
        saleteam_employees = get_sale_employee()

        next_index = (last_assigned_index + 1) % saleteam_employees.count()
        enquiry.assign_to_sales_employee = saleteam_employees[next_index]
        enquiry.lead_status = "PreEnrolled"
        enquiry.assign_to_sales_employee

        enquiry.save()
        cache.set("last_assigned_index", next_index)
        # return redirect("employee_leads")

    return redirect("employee_lead_list")


def enrolled_save(request, id):
    enquiry = Enquiry.objects.get(id=id)
    doc_id = enquiry.assign_to_documentation_employee
    if doc_id:
        enquiry.lead_status = "Enrolled"
        enquiry.save()

    last_assigned_index = cache.get("last_assigned_index") or 0
    documentation_team_employees = get_documentation_team_employee()
    if documentation_team_employees.exists():
        next_index = (last_assigned_index + 1) % documentation_team_employees.count()
        enquiry.assign_to_documentation_employee = documentation_team_employees[
            next_index
        ]
        enquiry.lead_status = "Enrolled"
        enquiry.save()
        cache.set("last_assigned_index", next_index)

    return redirect("employee_lead_list")


def enprocess_save(request, id):
    enquiry = Enquiry.objects.get(id=id)
    emp_doc_team = enquiry.assign_to_documentation_employee
    if emp_doc_team:
        enquiry.lead_status = "Inprocess"
        enquiry.save()

    last_assigned_index = cache.get("last_assigned_index") or 0
    visa_team_employees = get_visa_team_employee()

    if visa_team_employees.exists():
        next_index = (last_assigned_index + 1) % visa_team_employees.count()
        enquiry.assign_to_visa_team_employee = visa_team_employees[next_index]
        enquiry.lead_status = "Inprocess"
        enquiry.save()
        cache.set("last_assigned_index", next_index)

    return redirect("employee_lead_list")


def reject_save(request, id):
    enquiry = Enquiry.objects.get(id=id)
    enquiry.lead_status = "Reject"
    enquiry.save()
    return redirect("employee_lead_list")


def ready_to_submit_save(request, id):
    enquiry = Enquiry.objects.get(id=id)
    enquiry.lead_status = "Ready To Submit"
    enquiry.save()
    return redirect("employee_lead_list")


def appointment_save(request, id):
    enquiry = Enquiry.objects.get(id=id)
    enquiry.lead_status = "Appointment"
    enquiry.save()
    return redirect("employee_lead_list")


def ready_to_collection_save(request, id):
    enquiry = Enquiry.objects.get(id=id)
    enquiry.lead_status = "Ready To Collection"
    enquiry.save()
    return redirect("employee_lead_list")


def result_save(request, id):
    enquiry = Enquiry.objects.get(id=id)
    enquiry.lead_status = "Result"
    enquiry.save()
    return redirect("employee_lead_list")


def delivery_Save(request, id):
    enquiry = Enquiry.objects.get(id=id)
    enquiry.lead_status = "Delivery"
    enquiry.save()
    return redirect("employee_lead_list")


def enq_appointment_Save(request):
    if request.method == "POST":
        enq = request.POST.get("enq_id")
        enq_id = Enquiry.objects.get(id=enq)

        desc = request.POST.get("description")
        date = request.POST.get("date")
        time = request.POST.get("time")

        try:
            enqapp = EnqAppointment.objects.get(enquiry=enq_id)

            # Existing EnqAppointment found

            enqapp.description = desc
            enqapp.enquiry = enq_id
            enqapp.date = date
            enqapp.time = time
            enqapp.created_by = request.user
            enqapp.save()
        except EnqAppointment.DoesNotExist:
            # No existing EnqAppointment found, create a new one
            appt = EnqAppointment.objects.create(
                enquiry=enq_id,
                description=desc,
                date=date,
                time=time,
                created_by=request.user,
            )
            appt.save()

        return redirect("employee_lead_list")


def appointment_done(request, id):
    enq = Enquiry.objects.get(id=id)

    enq_appointment = EnqAppointment.objects.get(enquiry=enq)
    enq_appointment.status = "Done"

    enq_appointment.save()
    return redirect("employee_lead_list")


def get_public_ip():
    try:
        response = requests.get("https://api64.ipify.org?format=json")
        data = response.json()
        return data["ip"]
    except Exception as e:
        # Handle the exception (e.g., log the error)
        return None


def emp_add_notes(request):
    if request.method == "POST":
        enq_id = request.POST.get("enq_id")
        notes_text = request.POST.get("notes")
        file = request.FILES.get("file")
        user = request.user

        try:
            enq = Enquiry.objects.get(id=enq_id)
            ip_address = get_public_ip()

            notes = Notes.objects.create(
                enquiry=enq,
                notes=notes_text,
                file=file,
                ip_address=ip_address,
                created_by=user,
            )
            notes.save()

        except Enquiry.DoesNotExist:
            pass

    return redirect("employee_lead_list")


# ------------------------------------------ AGent Details --------------------------


def emp_add_agent(request):
    logged_in_user = request.user
    relevant_employees = Employee.objects.all()
    user = request.user

    dep = user.employee.department

    if request.method == "POST":
        type = request.POST.get("type")

        firstname = request.POST.get("firstname")
        lastname = request.POST.get("lastname")
        email = request.POST.get("email")
        contact = request.POST.get("contact")
        password = request.POST.get("password")
        country = request.POST.get("country")
        state = request.POST.get("state")
        city = request.POST.get("city")
        address = request.POST.get("address")
        zipcode = request.POST.get("zipcode")
        files = request.FILES.get("files")

        existing_agent = CustomUser.objects.filter(username=email)

        try:
            if existing_agent:
                messages.warning(request, f'"{email}" already exists.')
                return redirect("emp_add_agent")

            if type == "Outsourcing Partner":
                user = CustomUser.objects.create_user(
                    username=email,
                    first_name=firstname,
                    last_name=lastname,
                    email=email,
                    password=password,
                    user_type="5",
                )
                logged_in_user = request.user

                user.outsourcingagent.type = type
                user.outsourcingagent.contact_no = contact
                user.outsourcingagent.country = country
                user.outsourcingagent.state = state
                user.outsourcingagent.City = city
                user.outsourcingagent.Address = address
                user.outsourcingagent.zipcode = zipcode
                user.outsourcingagent.profile_pic = files
                user.outsourcingagent.registerdby = logged_in_user
                user.outsourcingagent.assign_employee = logged_in_user.employee

                user.save()

                subject = "Congratulations! Your Account is Created"
                message = (
                    f"Hello {firstname} {lastname},\n\n"
                    f"Welcome to SSDC \n\n"
                    f"Congratulations! Your account has been successfully created as an Outsource Agent.\n\n"
                    f" Your id is {email} and your password is {password}.\n\n"
                    f" go to login : https://crm.theskytrails.com/Agent/Login/ \n\n"
                    f"Thank you for joining us!\n\n"
                    f"Best regards,\nThe Sky Trails"
                )

                recipient_list = [email]

                send_mail(
                    subject, message, from_email=None, recipient_list=recipient_list
                )

                mobile_number = contact
                print("mobileeeee nobumber", mobile_number)
                message = (
                    f"Welcome to SSDC \n\n"
                    f"Congratulations! Your account has been successfully created as an Outsource Agent.\n\n"
                    f" Your id is {email} and your password is {password}.\n\n"
                    f" go to login : https://crm.theskytrails.com/ \n\n"
                    f"Thank you for joining us!\n\n"
                    f"Best regards,\nThe Sky Trails"
                )
                response = send_whatsapp_message(mobile_number, message)

                messages.success(request, "OutSource Agent Added Successfully")
                return redirect("emp_all_outsource_agent")

            else:
                user = CustomUser.objects.create_user(
                    username=email,
                    first_name=firstname,
                    last_name=lastname,
                    email=email,
                    password=password,
                    user_type="4",
                )
                logged_in_user = request.user

                user.agent.type = type
                user.agent.contact_no = contact
                user.agent.country = country
                user.agent.state = state
                user.agent.City = city
                user.agent.Address = address
                user.agent.zipcode = zipcode
                user.agent.profile_pic = files
                user.agent.registerdby = logged_in_user
                user.agent.assign_employee = logged_in_user.employee
                user.save()

                context = {"employees": relevant_employees, "dep": dep}

                subject = "Congratulations! Your Account is Created"
                message = (
                    f"Hello {firstname} {lastname},\n\n"
                    f"Welcome to SSDC \n\n"
                    f"Congratulations! Your account has been successfully created as an agent.\n\n"
                    f" Your id is {email} and your password is {password}.\n\n"
                    f" go to login : https://crm.theskytrails.com/Agent/Login/ \n\n"
                    f"Thank you for joining us!\n\n"
                    f"Best regards,\nThe Sky Trails"
                )

                recipient_list = [email]

                send_mail(
                    subject, message, from_email=None, recipient_list=recipient_list
                )

                mobile_number = contact

                message = (
                    f"Welcome to SSDC \n\n"
                    f"Congratulations! Your account has been successfully created as an agent.\n\n"
                    f" Your id is {email} and your password is {password}.\n\n"
                    f" go to login : https://crm.theskytrails.com/ \n\n"
                    f"Thank you for joining us!\n\n"
                    f"Best regards,\nThe Sky Trails"
                )
                response = send_whatsapp_message(mobile_number, message)

                messages.success(request, "Agent Added Successfully")
                return redirect("emp_agent_list")

        except Exception as e:
            messages.warning(request, e)

    context = {"employees": relevant_employees, "dep": dep}

    return render(request, "Employee/Agent Management/addagent.html", context)


class emp_all_agent(ListView):
    model = Agent
    template_name = "Employee/Agent Management/agentlist.html"
    context_object_name = "agent"

    def get_queryset(self):
        user = self.request.user.employee
        return Agent.objects.filter(assign_employee=user).order_by("-id")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        dep = user.employee.department
        context["employee_queryset"] = Employee.objects.all()
        context["dep"] = dep
        return context


class emp_allGrid_agent(ListView):
    model = Agent
    template_name = "Employee/Agent Management/agentgrid.html"
    context_object_name = "agent"

    def get_queryset(self):
        user = self.request.user.employee
        return Agent.objects.filter(assign_employee=user).order_by("-id")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        dep = user.employee.department
        context["employee_queryset"] = Employee.objects.all()
        context["dep"] = dep
        return context


def employee_agent_delete(request, id):
    agent = Agent.objects.get(id=id)
    agent.delete()
    messages.success(request, "Agent Deleted")
    return HttpResponseRedirect(reverse("emp_agent_list"))


def emp_agent_details(request, id):
    agent = Agent.objects.get(id=id)
    users = agent.users
    user = request.user
    dep = user.employee.department

    if request.method == "POST":
        firstname = request.POST.get("first_name")
        lastname = request.POST.get("last_name")

        dob = request.POST.get("dob")
        gender = request.POST.get("gender")
        maritial = request.POST.get("maritial")
        original_pic = request.FILES.get("original_pic")
        organization = request.POST.get("organization")
        business_type = request.POST.get("business_type")
        registration = request.POST.get("registration")
        address = request.POST.get("address")
        country = request.POST.get("country")
        state = request.POST.get("state")
        city = request.POST.get("city")
        zipcode = request.POST.get("zipcode")
        accountholder = request.POST.get("accountholder")
        bankname = request.POST.get("bankname")
        branchname = request.POST.get("branchname")
        account = request.POST.get("account")
        ifsc = request.POST.get("ifsc")

        print("first nameeee", firstname)

        if dob:
            users.agent.dob = dob
        if gender:
            users.agent.gender = gender
        if maritial:
            users.agent.marital_status = maritial
        if original_pic:
            users.agent.profile_pic = original_pic

        users.first_name = firstname

        users.agent.organization_name = organization
        users.agent.business_type = business_type
        users.agent.registration_number = registration
        users.agent.Address = address
        users.agent.country = country
        users.agent.state = state
        users.agent.City = city
        users.agent.zipcode = zipcode
        users.agent.account_holder = accountholder
        users.agent.bank_name = bankname
        users.agent.branch_name = branchname
        users.agent.account_no = account
        users.agent.ifsc_code = ifsc

        users.save()
        messages.success(request, "Updated Successfully")
        return redirect("emp_agent_details", id)

    context = {"agent": agent, "dep": dep}
    return render(request, "Employee/Agent Management/Update/agentupdate.html", context)


def employee_agent_agreement(request, id):
    agent = Agent.objects.get(id=id)
    user = request.user
    dep = user.employee.department
    agntagreement = AgentAgreement.objects.filter(agent=agent)
    if request.method == "POST":
        name = request.POST.get("agreement_name")
        file = request.FILES.get("file")
        agreement = AgentAgreement.objects.create(
            agent=agent, agreement_name=name, agreement_file=file
        )
        agreement.save()
        messages.success(request, "Agreement Updated Succesfully...")
        return redirect("employee_agent_agreement", id)
    context = {"agent": agent, "agreement": agntagreement, "dep": dep}
    return render(
        request, "Employee/Agent Management/Update/agentagreement.html", context
    )


def employee_agent_agreement_update(request, id):
    agree = AgentAgreement.objects.get(id=id)
    agent = agree.agent

    if request.method == "POST":
        agntagreement = AgentAgreement.objects.get(id=id)
        agreement_name = request.POST.get("agreement_name")
        file = request.FILES.get("file")

        agntagreement.agreement_name = agreement_name
        if file:
            agntagreement.agreement_file = file
        agntagreement.save()
        messages.success(request, "Agreement Updated Successfully...")
        return redirect("employee_agent_agreement", agent.id)


def emp_agent_agreement_delete(request, id):
    agree = AgentAgreement.objects.get(id=id)
    agent = agree.agent
    agreement = AgentAgreement.objects.get(id=id)
    agreement.delete()
    messages.success(request, "Agreement Deleted Successfully...")
    return redirect("employee_agent_agreement", agent.id)


def emp_agent_kyc(request, id):
    agent = Agent.objects.get(id=id)
    kyc_agent = AgentKyc.objects.filter(agent=agent).first
    user = request.user
    dep = user.employee.department
    # kyc_agent = get_object_or_404(AgentKyc, agent=agent)
    kyc_id = None

    if request.method == "POST":
        adharfront_file = request.FILES.get("adharfront_file")
        adharback_file = request.FILES.get("adharback_file")
        pan_file = request.FILES.get("pan_file")
        registration_file = request.FILES.get("registration_file")
        try:
            kyc_id = AgentKyc.objects.get(agent=agent)

            if kyc_id:
                if adharfront_file:
                    kyc_id.adhar_card_front = adharfront_file
                if adharback_file:
                    kyc_id.adhar_card_back = adharback_file
                if pan_file:
                    kyc_id.pancard = pan_file
                if registration_file:
                    kyc_id.registration_certificate = registration_file
                kyc_id.save()
                messages.success(request, "Kyc Added Successfully..")
                return redirect("admin_agent_kyc", id)
            else:
                print("workingggggggg")

        except AgentKyc.DoesNotExist:
            kyc_id = None
            kyc = AgentKyc.objects.create(
                agent=agent,
                adhar_card_front=adharfront_file,
                adhar_card_back=adharback_file,
                pancard=pan_file,
                registration_certificate=registration_file,
            )
            kyc.save()
            messages.success(request, "Kyc Added Successfully..")
            return redirect("emp_agent_kyc", id)

    context = {"agent": agent, "kyc_id": kyc_id, "kyc_agent": kyc_agent, "dep": dep}

    return render(request, "Employee/Agent Management/Update/agentkyc.html", context)


# ------------------------------ Outsource Agent --------------------------
class emp_all_outsource_agent(ListView):
    model = OutSourcingAgent
    template_name = "Employee/Agent Management/outsourcelist.html"
    context_object_name = "agentoutsource"

    def get_queryset(self):
        user = self.request.user.employee
        return OutSourcingAgent.objects.filter(assign_employee=user).order_by("-id")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        dep = user.employee.department
        context["dep"] = dep
        context["employee_queryset"] = Employee.objects.all()

        return context


class emp_allGrid_outsource_agent(ListView):
    model = OutSourcingAgent
    template_name = "Employee/Agent Management/outsorcegrid.html"
    context_object_name = "agentoutsource"

    def get_queryset(self):
        user = self.request.user.employee
        return OutSourcingAgent.objects.filter(assign_employee=user).order_by("-id")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        dep = user.employee.department
        context["dep"] = dep
        context["employee_queryset"] = Employee.objects.all()

        return context


def emp_outsourceagent_details(request, id):
    outsourceagent = OutSourcingAgent.objects.get(id=id)
    users = users = outsourceagent.users
    user = request.user
    dep = user.employee.department

    if request.method == "POST":
        firstname = request.POST.get("first_name")
        lastname = request.POST.get("last_name")

        dob = request.POST.get("dob")
        gender = request.POST.get("gender")
        maritial = request.POST.get("maritial")
        original_pic = request.FILES.get("original_pic")
        organization = request.POST.get("organization")
        business_type = request.POST.get("business_type")
        registration = request.POST.get("registration")
        address = request.POST.get("address")
        country = request.POST.get("country")
        state = request.POST.get("state")
        city = request.POST.get("city")
        zipcode = request.POST.get("zipcode")
        accountholder = request.POST.get("accountholder")
        bankname = request.POST.get("bankname")
        branchname = request.POST.get("branchname")
        account = request.POST.get("account")
        ifsc = request.POST.get("ifsc")

        if dob:
            users.outsourcingagent.dob = dob
        if gender:
            users.outsourcingagent.gender = gender
        if maritial:
            users.outsourcingagent.marital_status = maritial
        if original_pic:
            users.outsourcingagent.profile_pic = original_pic

        users.first_name = firstname

        users.outsourcingagent.organization_name = organization
        users.outsourcingagent.business_type = business_type
        users.outsourcingagent.registration_number = registration
        users.outsourcingagent.Address = address
        users.outsourcingagent.country = country
        users.outsourcingagent.state = state
        users.outsourcingagent.City = city
        users.outsourcingagent.zipcode = zipcode
        users.outsourcingagent.account_holder = accountholder
        users.outsourcingagent.bank_name = bankname
        users.outsourcingagent.branch_name = branchname
        users.outsourcingagent.account_no = account
        users.outsourcingagent.ifsc_code = ifsc

        users.save()
        messages.success(request, "Updated Successfully")
        return redirect("emp_outsourceagent_details", id)

    context = {"agent": outsourceagent, "dep": dep}
    return render(
        request,
        "Employee/Agent Management/OutsourceUpdate/outsource_agentupdate.html",
        context,
    )


def emp_outsource_agent_agreement(request, id):
    outsourceagent = OutSourcingAgent.objects.get(id=id)
    user = request.user
    dep = user.employee.department

    agntagreement = AgentAgreement.objects.filter(outsourceagent=outsourceagent)
    if request.method == "POST":
        name = request.POST.get("agreement_name")
        file = request.FILES.get("file")
        agreement = AgentAgreement.objects.create(
            outsourceagent=outsourceagent, agreement_name=name, agreement_file=file
        )
        agreement.save()
        messages.success(request, "Agreement Updated Succesfully...")
        return redirect("emp_outsource_agent_agreement", id)
    # context = {"agent": agent, "agreement": agntagreement}
    context = {"agent": outsourceagent, "agreement": agntagreement, "dep": dep}
    return render(
        request,
        "Employee/Agent Management/OutsourceUpdate/outsource_agentagreement.html",
        context,
    )


def emp_outsourceagent_agreement_update(request, id):
    if request.method == "POST":
        agntagreement = AgentAgreement.objects.get(id=id)
        outsource = agntagreement.outsourceagent
        agreement_name = request.POST.get("agreement_name")
        file = request.FILES.get("file")

        agntagreement.agreement_name = agreement_name
        if file:
            agntagreement.agreement_file = file
        agntagreement.save()
        messages.success(request, "Agreement Updated Successfully...")
        return redirect("emp_outsource_agent_agreement", outsource.id)


def emp_outsource_agent_agreement_delete(request, id):
    agree = AgentAgreement.objects.get(id=id)
    agent = agree.outsourceagent
    agreement = AgentAgreement.objects.get(id=id)
    agreement.delete()
    messages.success(request, "Agreement Deleted Successfully...")
    return redirect("emp_outsource_agent_agreement", agent.id)


def emp_outstsourceagent_delete(request, id):
    outsourceagent = OutSourcingAgent.objects.get(id=id)
    outsourceagent.delete()
    messages.success(request, "OutSourceAgent Deleted")
    return HttpResponseRedirect(reverse("emp_all_outsource_agent"))


def emp_outsource_agent_kyc(request, id):
    agent = OutSourcingAgent.objects.get(id=id)
    print("out soruce agent", id)
    kyc_agent = AgentKyc.objects.filter(outsourceagent=agent).first
    user = request.user
    dep = user.employee.department
    # kyc_agent = get_object_or_404(AgentKyc, agent=agent)
    kyc_id = None

    if request.method == "POST":
        adharfront_file = request.FILES.get("adharfront_file")
        adharback_file = request.FILES.get("adharback_file")
        pan_file = request.FILES.get("pan_file")
        registration_file = request.FILES.get("registration_file")
        try:
            kyc_id = AgentKyc.objects.get(outsourceagent=agent)

            if kyc_id:
                if adharfront_file:
                    kyc_id.adhar_card_front = adharfront_file
                if adharback_file:
                    kyc_id.adhar_card_back = adharback_file
                if pan_file:
                    kyc_id.pancard = pan_file
                if registration_file:
                    kyc_id.registration_certificate = registration_file
                kyc_id.save()
                messages.success(request, "Kyc Added Successfully..")
                return redirect("emp_outsource_agent_kyc", id)
            else:
                print("workingggggggg")

        except AgentKyc.DoesNotExist:
            kyc_id = None
            kyc = AgentKyc.objects.create(
                outsourceagent=agent,
                adhar_card_front=adharfront_file,
                adhar_card_back=adharback_file,
                pancard=pan_file,
                registration_certificate=registration_file,
            )
            kyc.save()
            messages.success(request, "Kyc Added Successfully..")
            return redirect("emp_outsource_agent_kyc", id)

    context = {"agent": agent, "kyc_id": kyc_id, "kyc_agent": kyc_agent, "dep": dep}

    return render(
        request,
        "Employee/Agent Management/OutsourceUpdate/outsource_agentkyc.html",
        context,
    )


# --------------------------------------- Enrolled ------------------------------


def emp_edit_enrolled_application(request, id):
    enquiry = Enquiry.objects.get(id=id)
    country = VisaCountry.objects.all()
    category = VisaCategory.objects.all()
    user = request.user
    dep = user.employee.department
    form = FollowUpForm()

    context = {
        "enquiry": enquiry,
        "country": country,
        "category": category,
        "dep": dep,
        "form": form,
    }

    if request.method == "POST":
        firstname = request.POST.get("firstname")
        lastname = request.POST.get("lastname")
        dob = request.POST.get("dob")
        try:
            dob_obj = datetime.strptime(dob, "%Y-%m-%d").date()
        except ValueError:
            dob_obj = None

        gender = request.POST.get("gender")
        maritialstatus = request.POST.get("maritialstatus")
        digitalsignature = request.FILES.get("digitalsignature")
        spouse_name = request.POST.get("spouse_name")
        spouse_no = request.POST.get("spouse_no")
        spouse_email = request.POST.get("spouse_email")
        spouse_passport = request.POST.get("spouse_passport")
        spouse_dob = request.POST.get("spouse_dob")
        try:
            spouse_dob_obj = datetime.strptime(spouse_dob, "%Y-%m-%d").date()
        except ValueError:
            spouse_dob_obj = None

        email = request.POST.get("email")
        contact = request.POST.get("contact")
        address = request.POST.get("address")
        city = request.POST.get("city")
        state = request.POST.get("state")
        Country = request.POST.get("Country")

        emergencyname = request.POST.get("emergencyname")
        emergencyphone = request.POST.get("emergencyphone")
        emergencyemail = request.POST.get("emergencyemail")
        applicantrelation = request.POST.get("applicantrelation")

        passportnumber = request.POST.get("passportnumber")
        issuedate = request.POST.get("issuedate")
        try:
            issuedate_obj = datetime.strptime(issuedate, "%Y-%m-%d").date()
        except ValueError:
            issuedate_obj = None

        expirydate = request.POST.get("expirydate")
        try:
            expirydate_obj = datetime.strptime(expirydate, "%Y-%m-%d").date()
        except ValueError:
            expirydate_obj = None

        issue_country = request.POST.get("issuecountry")
        birthcity = request.POST.get("birthcity")
        country_of_birth = request.POST.get("country_of_birth")

        nationality = request.POST.get("nationality")
        citizenship = request.POST.get("citizenships")
        more_than_one_country = request.POST.get("more_than_one_country")
        studyin_in_other_country = request.POST.get("studyin_in_other_country")

        citizenstatus = request.POST.get("citizenstatus")
        studystatus = request.POST.get("studystatus")

        citizen = request.POST.get("citizen")

        enquiry.FirstName = firstname
        enquiry.LastName = lastname
        enquiry.Dob = dob_obj
        enquiry.Gender = gender
        enquiry.marital_status = maritialstatus
        if digitalsignature:
            enquiry.digital_signature = digitalsignature
        enquiry.spouse_name = spouse_name
        enquiry.spouse_no = spouse_no
        enquiry.spouse_email = spouse_email
        enquiry.spouse_passport = spouse_passport
        enquiry.spouse_dob = spouse_dob_obj
        enquiry.email = email
        enquiry.contact = contact
        enquiry.Country = Country
        enquiry.state = state
        enquiry.city = city
        enquiry.address = address

        enquiry.passport_no = passportnumber
        enquiry.issue_date = issuedate_obj
        enquiry.expirty_Date = expirydate_obj
        enquiry.issue_country = issue_country
        enquiry.city_of_birth = birthcity
        enquiry.country_of_birth = country_of_birth
        enquiry.nationality = nationality
        enquiry.citizenship = citizenship
        enquiry.more_than_one_country = more_than_one_country
        enquiry.studyin_in_other_country = studyin_in_other_country
        enquiry.emergency_name = emergencyname
        enquiry.emergency_phone = emergencyphone
        if emergencyemail != "None":
            enquiry.emergency_email = emergencyemail
        enquiry.relation_With_applicant = applicantrelation
        enquiry.save()
        messages.success(request, "Persoanal Details Updated Successfully....")

        return redirect("emp_edit_enrolled_application", id)

    return render(
        request,
        "Employee/Enquiry/Enrolled Enquiry/Editenrolledpart1.html",
        context,
    )


def emp_combined_view(request, id):
    enquiry = get_object_or_404(Enquiry, id=id)
    edu_sum = Education_Summary.objects.filter(enquiry_id=enquiry).first
    work_exp = Work_Experience.objects.filter(enquiry_id=enquiry).first
    bk_info = Background_Information.objects.filter(enquiry_id=enquiry).first
    user = request.user
    dep = user.employee.department

    if request.method == "POST":
        # Education Summary
        education_summary, created = Education_Summary.objects.get_or_create(
            enquiry_id=enquiry
        )
        education_summary.highest_level_education = request.POST.get(
            "highest_education"
        )
        education_summary.grading_scheme = request.POST.get("gradingscheme")
        education_summary.grade_avg = request.POST.get("gradeaverage")
        education_summary.recent_college = request.POST.get("recent_college")
        education_summary.country_of_education = request.POST.get("educationcountry")
        education_summary.country_of_institution = request.POST.get("institutecountry")
        education_summary.name_of_institution = request.POST.get("institutename")
        education_summary.primary_language = request.POST.get("instructionlanguage")
        education_summary.institution_from = request.POST.get("institutionfrom")
        try:
            education_summary.institution_from_obj = datetime.strptime(
                education_summary.institution_from, "%Y-%m-%d"
            ).date()
        except ValueError:
            education_summary.institution_from = None
        education_summary.institution_to = request.POST.get("institutionto")
        try:
            education_summary.institution_to_obj = datetime.strptime(
                education_summary.institution_to, "%Y-%m-%d"
            ).date()
        except ValueError:
            education_summary.institution_to = None
        education_summary.degree_Awarded = request.POST.get("degreeawarded")
        education_summary.degree_Awarded_On = request.POST.get("degreeawardedon")
        education_summary.save()

        # Test Score
        examtype = request.POST.get("examtype")
        exam_date = request.POST.get("examdate")

        try:
            exam_date = datetime.strptime(exam_date, "%Y-%m-%d").date()
        except ValueError:
            exam_date = None
        reading = request.POST.get("reading")
        listening = request.POST.get("listening")
        speaking = request.POST.get("speaking")
        writing = request.POST.get("writing")
        overall_score = request.POST.get("overallscore")

        existing_test_score = TestScore.objects.filter(
            exam_type=examtype, enquiry_id=enquiry
        ).first()
        if reading or exam_date or listening or speaking or writing or overall_score:
            if existing_test_score is None:
                test_scores = TestScore.objects.create(
                    enquiry_id=enquiry,
                    exam_type=examtype,
                    exam_date=exam_date,
                    reading=reading,
                    listening=listening,
                    speaking=speaking,
                    writing=writing,
                    overall_score=overall_score,
                )

            else:
                existing_test_score.exam_date = exam_date
                existing_test_score.reading = reading
                existing_test_score.listening = listening
                existing_test_score.speaking = speaking
                existing_test_score.writing = writing
                existing_test_score.overall_score = overall_score
                existing_test_score.save()

        # Handle Background Information
        background_info, created = Background_Information.objects.get_or_create(
            enquiry_id=enquiry
        )
        background_info.background_information = request.POST.get("australliabefore")
        background_info.save()

        # Handle Work Experience
        work_exp, created = Work_Experience.objects.get_or_create(enquiry_id=enquiry)
        work_exp.company_name = request.POST.get("companyname")
        work_exp.designation = request.POST.get("designation")
        work_exp.from_date = request.POST.get("fromdate")
        try:
            work_exp.from_date_obj = datetime.strptime(
                work_exp.from_date, "%Y-%m-%d"
            ).date()
        except ValueError:
            work_exp.from_date = None
        work_exp.to_date = request.POST.get("todate")
        try:
            work_exp.to_date_obj = datetime.strptime(
                work_exp.to_date, "%Y-%m-%d"
            ).date()
        except ValueError:
            work_exp.to_date = None
        work_exp.address = request.POST.get("address")
        work_exp.city = request.POST.get("city")
        work_exp.state = request.POST.get("state")
        work_exp.describe = request.POST.get("workdetails")
        work_exp.save()

        return redirect("emp_education_summary", id)

    test_scores = TestScore.objects.filter(enquiry_id=enquiry)

    context = {
        "enquiry": enquiry,
        "test_scores": test_scores,
        "education_summary": edu_sum,
        "work_exp": work_exp,
        "bk_info": bk_info,
        "dep": dep,
    }

    return render(
        request, "Employee/Enquiry/Enrolled Enquiry/Editenrolledpart2.html", context
    )


def emp_editproduct_details(request, id):
    enquiry = Enquiry.objects.get(id=id)
    country = VisaCountry.objects.all()
    category = VisaCategory.objects.all()
    product = Package.objects.all()
    user = request.user
    dep = user.employee.department
    context = {
        "enquiry": enquiry,
        "country": country,
        "category": category,
        "product": product,
        "dep": dep,
    }

    if request.method == "POST":
        source = request.POST.get("source")
        reference = request.POST.get("reference")
        visatype = request.POST.get("visatype")
        visacountry_id = request.POST.get("visacountry_id")
        visacategory_id = request.POST.get("visacategory_id")
        visasubcategory_id = request.POST.get("visasubcategory")
        product_id = request.POST.get("Package")

        visa_country = VisaCountry.objects.get(id=visacountry_id)
        visa_category = VisaCategory.objects.get(id=visacategory_id)
        visa_subcategory = VisaCategory.objects.get(id=visacategory_id)
        package = Package.objects.get(id=product_id)

        enquiry.Source = source
        enquiry.Reference = reference
        enquiry.Visa_type = visatype
        enquiry.Visa_country = visa_country
        enquiry.Visa_category = visa_category
        enquiry.Visa_subcategory = visa_subcategory
        enquiry.Package = package

        enquiry.save()

        return redirect("emp_editproduct_details", id=id)

    return render(
        request,
        "Employee/Enquiry/Enrolled Enquiry/Editenrolledpart3.html",
        context,
    )


def emp_enrolleddocument(request, id):
    enq = Enquiry.objects.get(id=id)
    document = Document.objects.all()
    user = request.user
    dep = user.employee.department

    doc_file = DocumentFiles.objects.filter(enquiry_id=enq)

    case_categories = CaseCategoryDocument.objects.filter(country=enq.Visa_country)

    documents_prefetch = Prefetch(
        "document",
        queryset=Document.objects.select_related("document_category", "lastupdated_by"),
    )

    case_categories = case_categories.prefetch_related(documents_prefetch)

    grouped_documents = {}

    for case_category in case_categories:
        for document in case_category.document.all():
            document_category = document.document_category
            testing = document.document_category.id

            if document_category not in grouped_documents:
                grouped_documents[document_category] = []

            grouped_documents[document_category].append(document)

    context = {
        "enq": enq,
        "grouped_documents": grouped_documents,
        "doc_file": doc_file,
        "dep": dep,
    }

    return render(
        request, "Employee/Enquiry/Enrolled Enquiry/Editenrolledpart4.html", context
    )


def emp_enrolled_upload_document(request):
    if request.method == "POST":
        try:
            document_id = request.POST.get("document_id")
            enq_id = request.POST.get("enq_id")

            document = Document.objects.get(pk=document_id)
            document_file = request.FILES.get("document_file")
            enq = Enquiry.objects.get(id=enq_id)

            # Check if a DocumentFiles object with the same document exists
            doc = DocumentFiles.objects.filter(
                enquiry_id=enq_id, document_id=document
            ).first()

            if doc:
                doc.document_file = document_file
                doc.lastupdated_by = request.user
                doc.save()

                return redirect("enrolled_document", id=enq_id)
            else:
                document_files = DocumentFiles.objects.create(
                    document_file=document_file,
                    document_id=document,
                    enquiry_id=enq,
                    lastupdated_by=request.user,
                )
                document_files.save()

                return redirect("emp_enrolleddocument", id=enq_id)

        except Exception as e:
            pass


def emp_enrolled_delete_docfile(request, id):
    doc_id = DocumentFiles.objects.get(id=id)
    enq_id = Enquiry.objects.get(id=doc_id.enquiry_id.id)
    enqq = enq_id.id

    doc_id.delete()
    return redirect("emp_enrolleddocument", enqq)


# ------------------------- Followup ---------------------------


def followup(request):
    if request.method == "POST":
        enq = request.POST.get("enq_id")
        enquiry = Enquiry.objects.get(id=enq)

        follow_up_form = FollowUpForm(request.POST)
        if follow_up_form.is_valid():
            follow_up = follow_up_form.save(commit=False)
            follow_up.enquiry = enquiry
            follow_up.created_by = request.user
            follow_up.save()
            messages.success(request, "Followup Created Successfully")
            return redirect("emp_edit_enrolled_application", enquiry.id)


def emp_followup_list(request):
    user = request.user.employee
    user2 = request.user
    form = FollowUpForm()
    priority = PRIORITY_CHOICES
    status = FOLLOWUP_STATUS_CHOICES

    enq_list = Enquiry.objects.filter(
        # Q(created_by=user)
        Q(assign_to_employee=user)
        | Q(assign_to_sales_employee=user)
        | Q(assign_to_documentation_employee=user)
        | Q(assign_to_visa_team_employee=user)
    ).distinct()
    followup = FollowUp.objects.filter(enquiry__in=enq_list)
    print("follow up", followup)
    context = {
        "followup": followup,
        "form": form,
        "priority": priority,
        "status": status,
    }
    return render(request, "Employee/FollowUp/followup_list.html", context)


def followup_update(request):
    if request.method == "POST":
        followup_id = request.POST.get("followup_id")
        title = request.POST.get("title")
        description = request.POST.get("description")
        date = request.POST.get("date")
        time = request.POST.get("time")
        follow_up_status = request.POST.get("follow_up_status")
        priority = request.POST.get("priority")
        remark = request.POST.get("remark")

        followup = FollowUp.objects.get(id=followup_id)

        followup.title = title
        followup.description = description
        followup.follow_up_status = follow_up_status
        followup.priority = priority
        followup.calendar = date
        followup.time = time
        followup.remark = remark
        followup.save()
        messages.success(request, "Followup Updated Successfully...")

        return redirect("emp_followup_list")


def emp_followup_delete(request, id):
    followup = FollowUp.objects.get(id=id)
    followup.delete()
    messages.success(request, "Followup Deleted... !!")
    return redirect(emp_followup_list)


###################################### LOGOUT #######################################################


@login_required
def employee_logout(request):
    logout(request)
    return redirect("/")


############################################### CHANGE PASSWORD ###########################################


@login_required
def ChangePassword(request):
    user = request.user
    admin = Employee.objects.get(users=user)

    if request.method == "POST":
        old_psw = request.POST.get("old_password")
        newpassword = request.POST.get("newpassword")
        confirmpassword = request.POST.get("confirmpassword")

        if check_password(old_psw, admin.users.password):
            if newpassword == confirmpassword:
                admin.users.set_password(newpassword)
                admin.users.save()
                messages.success(
                    request, "Password changed successfully Please Login Again !!"
                )
                return HttpResponseRedirect(reverse("login"))
            else:
                messages.success(request, "New passwords do not match")
                return HttpResponseRedirect(reverse("login"))

        else:
            messages.warning(request, "Old password is not correct")
            return HttpResponseRedirect(reverse("login"))

    return render(request, "Employee/Dashboard/dashboard.html")


# ----------------------------------------- FAQ ------------------------


class emp_FAQCreateView(LoginRequiredMixin, CreateView):
    model = FAQ
    form_class = FAQForm
    template_name = "Employee/Queries/add_query.html"
    success_url = reverse_lazy("emp_ResolvedFAQListView")

    def form_valid(self, form):
        form.instance.user = self.request.user

        messages.success(self.request, "FAQ Added Successfully.")

        return super().form_valid(form)


# def get_pending_queries_count(request):
#     user = request.user
#     return FAQ.objects.filter(user=user, answer__exact='').exclude(answer__isnull=True)


def get_pending_queries_count():
    return FAQ.objects.filter(answer__exact="").exclude(answer__isnull=True).count()


class queirylist(LoginRequiredMixin, ListView):
    model = FAQ
    template_name = "Employee/Queries/Queries.html"
    context_object_name = "resolved_queries"

    def get_queryset(self):
        return FAQ.objects.all().exclude(answer="")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pending_queries_count"] = get_pending_queries_count()
        return context


class pending_queirylist(LoginRequiredMixin, ListView):
    model = FAQ
    template_name = "Employee/Queries/PendingQueries.html"
    context_object_name = "pending_queries"

    def get_queryset(self):
        return FAQ.objects.all().exclude(answer__isnull=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        faq_emp_wise = FAQ.objects.filter(employee=user.employee)

        print("ggggggggggggg", faq_emp_wise)
        context["pending_queries_count"] = self.get_queryset().count()
        context["faq_emp_wise"] = faq_emp_wise
        return context


def emp_faq_ans(request, id):
    faq = FAQ.objects.get(id=id)
    if request.method == "POST":
        answer = request.POST.get("answer")
        faq.answer = answer
        faq.save()
        return redirect("emppending_queirylist")


def emp_ResolvedFAQListView(request):
    faq = FAQ.objects.all()
    pending = FAQ.objects.filter(answer__exact="").count()

    print("pendinggg", pending)
    context = {"faq": faq, "pending": pending}
    return render(request, "Employee/Queries/resolvedquery.html", context)


# class emp_ResolvedFAQListView(LoginRequiredMixin, ListView):
#     model = FAQ
#     template_name = "Employee/Queries/resolvedquery.html"
#     context_object_name = "emp_ResolvedFAQListView"

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["pending_queries_count"] = self.get_pending_queries_count(
#             self.request.user
#         )
#         return context

#     def get_pending_queries_count(self, user):
#         return (
#             FAQ.objects.filter(user=user, answer__exact="")
#             .exclude(answer__isnull=True)
#             .count()
#         )


def emp_PendingFAQListView(request):
    faq = FAQ.objects.all()
    pending = FAQ.objects.filter(answer__exact="").count()

    print("pendinggg", pending)
    context = {"faq": faq, "pending": pending}

    # pending_queries = FAQ.objects.filter(user=request.user, answer__exact="").exclude(
    #     answer__isnull=True
    # )
    # pending_queries_count = pending_queries.count()
    # context = {
    #     "pending_queries": pending_queries,
    #     "pending_queries_count": pending_queries_count,
    # }

    return render(request, "Employee/Queries/quries.html", context)


# class emp_PendingFAQListView(LoginRequiredMixin, ListView):
#     model = FAQ
#     template_name = "Employee/Queries/quries.html"
#     context_object_name = "pending_queries"

#     def get_queryset(self):
#         return FAQ.objects.filter(user=self.request.user, answer__exact="").exclude(
#             answer__isnull=True
#         )

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["pending_queries_count"] = self.get_queryset().count()
#         return context

################################################## PRODUCT ################################################


class PackageListView(LoginRequiredMixin, ListView):
    model = Package
    template_name = "Employee/Product/product.html"
    context_object_name = "Package"

    def get_queryset(self):
        return Package.objects.order_by("-id")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user
        dep = user.employee.department
        context["dep"] = dep

        return context


class PackageDetailView(LoginRequiredMixin, DetailView):
    model = Package
    template_name = "Employee/Product/Productdetails.html"
    context_object_name = "package"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user
        dep = user.employee.department
        context["dep"] = dep

        return context


class profileview(TemplateView, LoginRequiredMixin):
    template_name = "Employee/Profile/Profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        leads = Enquiry.objects.filter(created_by=self.request.user)
        # employee = Employee.objects.all()
        agent = Agent.objects.filter(assign_employee=self.request.user.employee).count()
        # agent = Agent.objects.get(assign_employee__user=self.request.user)

        user = self.request.user
        dep = user.employee.department
        context["dep"] = dep

        context["first_name"] = user.first_name
        context["last_name"] = user.last_name
        context["email"] = user.email
        context["contact"] = user.employee.contact_no

        context["department"] = user.employee.department
        if hasattr(user, "get_user_type_display"):
            context["user_type"] = user.get_user_type_display()
        context["leads"] = leads
        context["agent"] = agent
        context["emp_code"] = user.employee.emp_code

        return context


@login_required
def edit_profile(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        contact = request.POST.get("contact")

        employee_instance = Employee.objects.get(users=request.user)

        employee_instance.users.first_name = first_name
        employee_instance.users.last_name = last_name
        employee_instance.contact_no = contact

        employee_instance.users.save()
        employee_instance.save()

        return redirect("Employee_profile")

    return render(request, "Employee/Profile/Profile.html")
