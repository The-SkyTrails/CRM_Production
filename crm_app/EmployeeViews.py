from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import CreateView, ListView, UpdateView, DetailView
from .forms import *
from django.urls import reverse_lazy
from django.db.models import Prefetch
import requests


def employee_dashboard(request):
    return render(request, "Employee/Dashboard/dashboard.html")


def employee_profile(request):
    return render(request, "Employee/Profile/Profile.html")


def employee_query_list(request):
    return render(request, "Employee/Queries/querieslist.html")


def employee_pending_query(request):
    return render(request, "Employee/Queries/pending_query.html")


def employee_followup_list(request):
    return render(request, "Employee/FollowUp/followup_list.html")


class emp_Enquiry1View(CreateView):
    def get(self, request):
        form = EnquiryForm1()
        return render(
            request,
            "Employee/Enquiry/lead1.html",
            {"form": form},
        )

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


class emp_Enquiry2View(CreateView):
    def get(self, request):
        form = EnquiryForm2()
        return render(
            request,
            "Employee/Enquiry/lead2.html",
            {"form": form},
        )

    def post(self, request):
        form = EnquiryForm2(request.POST)
        if form.is_valid():
            # Retrieve personal details from session
            enquiry_form1 = request.session.get("enquiry_form1", {})
            cleaned_data = {
                "spouse_name": form.cleaned_data["spouse_name"],
                "spouse_no": form.cleaned_data["spouse_no"],
                "spouse_email": form.cleaned_data["spouse_email"],
                "spouse_passport": form.cleaned_data["spouse_passport"],
                "spouse_dob": form.cleaned_data["spouse_dob"].strftime("%Y-%m-%d"),
            }

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


class emp_Enquiry3View(CreateView):
    def get(self, request):
        form = EnquiryForm3()
        return render(
            request,
            "Employee/Enquiry/lead3.html",
            {"form": form},
        )

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
            print("usersssss", user)
            emp_dep = user.employee
            print("departttttttttttttttttttttt", emp_dep.department)
            if emp_dep.department == "Presales/Assesment":
                enquiry.assign_to_employee = self.request.user.employee
                print("workingggggggggggg")

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


def empdocument(request, id):
    enq = Enquiry.objects.get(id=id)
    document = Document.objects.all()

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
    }

    return render(request, "Employee/Enquiry/lead4.html", context)


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


def emp_delete_docfile(request, id):
    doc_id = DocumentFiles.objects.get(id=id)
    enq_id = Enquiry.objects.get(id=doc_id.enquiry_id.id)
    enqq = enq_id.id

    doc_id.delete()
    return redirect("emp_enquiry_form4", enqq)


# -------------------------------------- Leads ------------------------------


def employee_lead_list(request):
    user = request.user
    if user.is_authenticated:
        if user.user_type == "3":
            emp = user.employee
            dep = emp.department
            if dep == "Presales/Assesment":
                enq = Enquiry.objects.filter(assign_to_employee=user.employee)
            elif dep == "Sales":
                enq = Enquiry.objects.filter(assign_to_sales_employee=user.employee)
            elif dep == "Documentation":
                enq = Enquiry.objects.filter(
                    assign_to_documentation_employee=user.employee
                )
            elif dep == "Visa Team":
                enq = Enquiry.objects.filter(assign_to_visa_team_employee=user.employee)
            else:
                enq = None
            print("enquiryyyyy", enq)
            context = {"enq": enq, "user": user, "dep": dep}
    return render(request, "Employee/Enquiry/lead_list.html", context)


def employee_lead_grid(request):
    return render(request, "Employee/Enquiry/lead-grid.html")


def employee_lead_details(request):
    return render(request, "Employee/Enquiry/lead-details.html")


def employee_other_details(request):
    return render(request, "Employee/Enquiry/other-details.html")


def employee_product_selection(request):
    return render(request, "Employee/Enquiry/Product-Selection.html")


def employee_lead_documents(request):
    return render(request, "Employee/Enquiry/documents.html")


def employee_enrolled_lead(request):
    return render(request, "Employee/Enquiry/Enrolledleads.html")


def employee_enrolled_grid(request):
    return render(request, "Employee/Enquiry/enroll_lead-grid.html")


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
        print("workingggg")

        enq = request.POST.get("enq_id")
        enq_id = Enquiry.objects.get(id=enq)
        print("enquirry iddd", enq_id)
        desc = request.POST.get("description")
        date = request.POST.get("date")
        time = request.POST.get("time")

        try:
            enqapp = EnqAppointment.objects.get(enquiry=enq_id)
            print("heloooo", enqapp)

            # Existing EnqAppointment found
            print("wprloooooooooooooo")
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
