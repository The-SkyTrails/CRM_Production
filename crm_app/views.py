from django.shortcuts import render, redirect

# Create your views here.


def home(request):
    return render(request, "index.html")


# views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import Step1Form, Step2Form, Step3Form


@csrf_exempt  # Remove this if you have a better way to handle CSRF protection
def submit_form(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        print("password", password)

        # Process the form data as needed
        # Perform validation, save to the database, etc.

        # Return a JSON response indicating success
        return JsonResponse({"success": True})

    # Return a JSON response indicating failure if the request method is not POST
    return JsonResponse({"success": False})


def multi_step_form(request):
    if request.method == "POST":
        if "step1_submit" in request.POST:
            form = Step1Form(request.POST)
            if form.is_valid():
                # Store data from Step 1 in session
                request.session["step1_data"] = form.cleaned_data
                return redirect("multi_step_form_step2")
        elif "step2_submit" in request.POST:
            form = Step2Form(request.POST)
            if form.is_valid():
                # Update data from Step 2 in session
                request.session["step1_data"].update(form.cleaned_data)
                return redirect("multi_step_form_step3")
        elif "step3_submit" in request.POST:
            form = Step3Form(request.POST)
            if form.is_valid():
                # Combine all steps' data and process it
                data = request.session.get("step1_data", {}).copy()
                data.update(form.cleaned_data)

                # Clear session data
                del request.session["step1_data"]

                # Process or save the data as needed
                # For demonstration purposes, printing the data
                print("Form submitted successfully:", data)

                return redirect("success_page")  # Redirect to a success page
    else:
        form = Step1Form()

    return render(request, "multi_step_form.html", {"form": form})
