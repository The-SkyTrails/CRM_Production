import requests
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.utils import timezone
from .models import (
    CustomUser,
    LoginLog,
    Employee,
    Agent,
    OutSourcingAgent,
    Admin,
    ChatGroup,
    ChatMessage,
)
from .doubletick import whatsapp_signup_mes
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from rest_framework import viewsets
import random
from django.db.utils import IntegrityError
from django.core.mail import send_mail
from .SMSAPI.whatsapp_api import send_whatsapp_message, send_sms_message
from django.http import JsonResponse
from django.core.cache import cache
from django.template import loader
from .Email.email_utils import send_congratulatory_email
from django.views.decorators.csrf import csrf_protect


def get_public_ip():
    try:
        response = requests.get("https://api64.ipify.org?format=json")
        data = response.json()
        return data["ip"]
    except Exception as e:
        return None


def agent_signup(request):
    if request.method == "POST":
        user_type = request.POST.get("type")
        firstname = request.POST.get("firstname")
        lastname = request.POST.get("lastname")
        email = request.POST.get("email")
        contact_no = request.POST.get("contact_no")
        password = request.POST.get("password")

        existing_agent = CustomUser.objects.filter(email=email)
        last_assigned_index = cache.get("last_assigned_index") or 0
        sales_team_employees = Employee.objects.filter(department="Sales")
        fullname = str(firstname + lastname)
        request.session["mobile"] = contact_no

        try:
            if existing_agent:
                messages.warning(request, f'"{email}" already exists.')
                return render(request, "Login/Signuppage.html")

            if user_type == "Outsourcing partner":
                user = CustomUser.objects.create_user(
                    username=email,
                    first_name=firstname,
                    last_name=lastname,
                    email=email,
                    password=password,
                    user_type="5",
                )

                user.outsourcingagent.type = user_type
                user.outsourcingagent.contact_no = contact_no
                if sales_team_employees.exists():
                    next_index = (
                        last_assigned_index + 1
                    ) % sales_team_employees.count()
                    user.outsourcingagent.assign_employee = sales_team_employees[
                        next_index
                    ]

                    chat_group_name = f"{fullname} Group"
                    chat_group = ChatGroup.objects.create(
                        group_name=chat_group_name,
                    )
                    chat_group.group_member.add(
                        user.outsourcingagent.assign_employee.users
                    )
                    chat_group.group_member.add(user)
                    cache.set("last_assigned_index", next_index)

                user.save()
                messages.success(request, "OutsourceAgent Added Successfully")

                mobile = contact_no
                try:
                    whatsapp_signup_mes(
                        firstname, lastname, email, password, mobile, user_type="5"
                    )
                except:
                    pass

                send_congratulatory_email(
                    firstname, lastname, email, password, user_type
                )

                request.session["username"] = email
                request.session["password"] = password

            else:
                user2 = CustomUser.objects.create_user(
                    username=email,
                    first_name=firstname,
                    last_name=lastname,
                    email=email,
                    password=password,
                    user_type="4",
                )

                user2.agent.type = user_type
                user2.agent.contact_no = contact_no
                if sales_team_employees.exists():
                    next_index = (
                        last_assigned_index + 1
                    ) % sales_team_employees.count()
                    user2.agent.assign_employee = sales_team_employees[next_index]

                    chat_group_name = f"{fullname} Group"
                    chat_group = ChatGroup.objects.create(
                        group_name=chat_group_name,
                    )
                    chat_group.group_member.add(user2.agent.assign_employee.users)
                    chat_group.group_member.add(user2)
                    cache.set("last_assigned_index", next_index)

                user2.save()

                messages.success(request, "Agent Added Successfully")
                send_congratulatory_email(
                    firstname, lastname, email, password, user_type
                )
                mobile = contact_no
                try:
                    whatsapp_signup_mes(
                        firstname, lastname, email, password, mobile, user_type="4"
                    )
                except:
                    pass

                request.session["username"] = email
                request.session["password"] = password
                request.session["contact_no"] = contact_no

            # Send OTP via SMS for both user types
            random_number = random.randint(0, 99999)
            send_otp = str(random_number).zfill(6)
            request.session["sendotp"] = send_otp

            if user_type == "4":
                contact_no = user2.agent.contact_no
            elif user_type == "5":
                contact_no = user.outsourcingagent.contact_no

            url = "http://sms.txly.in/vb/apikey.php"
            payload = {
                "apikey": "lbwUbocDLNFjenpa",
                "senderid": "SKTRAL",
                "templateid": "1007338024565017323",
                "number": contact_no,
                "message": f"Use this OTP {send_otp} to login to your theskytrails account",
            }
            response = requests.post(url, data=payload)

            return redirect("verify_otp")

        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")

    return render(request, "Login/Signuppage.html")


@csrf_protect
def verify_otp(request):
    mobile = request.session.get("mobile", "Default value if key does not exist")

    last_three_digits = str(mobile)[-3:]

    if request.method == "POST":
        num1 = request.POST.get("num1")
        num2 = request.POST.get("num2")
        num3 = request.POST.get("num3")
        num4 = request.POST.get("num4")
        num5 = request.POST.get("num5")
        num6 = request.POST.get("num6")
        submitted_otp = num1 + num2 + num3 + num4 + num5 + num6

        username = request.session.get(
            "username", "Default value if key does not exist"
        )
        password = request.session.get(
            "password", "Default value if key does not exist"
        )
        sendotp = request.session.get("sendotp", "Default value if key does not exist")

        # submitted_otp = request.POST.get("submitted_otp")

        # if submitted_otp == sendotp:
        if submitted_otp == sendotp:
            user = authenticate(request, username=username, password=password)

            if user != None:
                login(request, user)
                user_type = user.user_type
                if user_type == "1":
                    return redirect("dashboard")
                if user_type == "2":
                    return redirect("admin_dashboard")
                if user_type == "3":
                    user.is_logged_in = True
                    user.save()
                    return redirect("employee_dashboard")
                if user_type == "4":
                    user.is_logged_in = True
                    user.save()
                    return redirect("agent_dashboard")
                if user_type == "5":
                    user.is_logged_in = True
                    user.save()
                    return redirect("agent_dashboard")

                public_ip = get_public_ip()
                LoginLog.objects.create(
                    user=user,
                    ip_address=public_ip if public_ip else None,
                    login_datetime=timezone.now(),
                    # date = timezone.now()
                )

        else:
            messages.error(request, "Wrong OTP")

    context = {"last_three_digits": last_three_digits}

    return render(request, "Login/Otp.html", context)


def CustomLoginView(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        request.session["username"] = username
        request.session["password"] = password

        try:
            user = CustomUser.objects.get(username=username)

            if check_password(password, user.password):
                user_type = user.user_type

                if user_type == "1":
                    # If user_type is "1" (HOD), log in directly
                    user = authenticate(request, username=username, password=password)

                    if user is not None:
                        login(request, user)
                        return redirect("SuperAdmin/crm/dashboard/")

                elif user_type in ("2", "3", "4", "5"):
                    public_ip = get_public_ip()
                    LoginLog.objects.create(
                        user=user,
                        ip_address=public_ip if public_ip else None,
                        login_datetime=timezone.now(),
                        # date = timezone.now()
                    )
                    # If user_type is "2" (Admin) or "3" (Employee), proceed with OTP verification
                    request.session["username"] = username
                    request.session["password"] = password
                    user_id = user.id
                    mob = ""
                    customeruser = CustomUser.objects.get(id=user_id)
                    user_type = customeruser.user_type
                    if user_type == "2":
                        mob = customeruser.admin.contact_no

                    if user_type == "3":
                        mob = customeruser.employee.contact_no

                    if user_type == "4":
                        mob = customeruser.agent.contact_no

                    if user_type == "5":
                        mob = customeruser.outsourcingagent.contact_no

                    request.session["mobile"] = mob
                    random_number = random.randint(0, 99999)
                    send_otp = str(random_number).zfill(6)
                    request.session["sendotp"] = send_otp
                    print("senddddd ot", send_otp)
                    url = "http://sms.txly.in/vb/apikey.php"
                    payload = {
                        "apikey": "lbwUbocDLNFjenpa",
                        "senderid": "SKTRAL",
                        "templateid": "1007338024565017323",
                        "number": mob,
                        "message": f"Use this OTP {send_otp} to login to your. theskytrails account",
                    }
                    response = requests.post(url, data=payload)

                    # send_otp_and_redirect(request, user_id, user_type)
                    # return redirect("verify_otp")
                    return redirect("verify_otp")
                else:
                    return HttpResponse("User type not supported")

            else:
                messages.error(request, "Username and Password Incorrect")
                return redirect("login")

        except CustomUser.DoesNotExist:
            messages.error(request, "User Does Not Exist")
            return redirect("login")
            # return HttpResponse("Username and Password Incorrect")

    return render(request, "Login/Login.html")


def resend_otp(request):
    username = request.session.get("username")
    password = request.session.get("password")

    if username and password:
        try:
            user = CustomUser.objects.get(username=username)

            if check_password(password, user.password):
                user_type = user.user_type

                # Rest of your logic for user types and sending OTP
                if user_type in ("2", "3", "4", "5"):
                    mob = ""

                    if user_type == "2":
                        mob = user.admin.contact_no
                    elif user_type == "3":
                        mob = user.employee.contact_no
                    elif user_type == "4":
                        mob = user.agent.contact_no
                    elif user_type == "5":
                        mob = user.outsourcingagent.contact_no

                    random_number = random.randint(0, 99999)
                    send_otp = str(random_number).zfill(6)
                    request.session["sendotp"] = send_otp

                    url = "http://sms.txly.in/vb/apikey.php"
                    payload = {
                        "apikey": "lbwUbocDLNFjenpa",
                        "senderid": "SKTRAL",
                        "templateid": "1007338024565017323",
                        "number": mob,
                        "message": f"Use this OTP {send_otp} to login to your. theskytrails account",
                    }
                    print("New OTp ", send_otp)
                    response = requests.post(url, data=payload)
                    return redirect("verify_otp")

        except CustomUser.DoesNotExist:
            pass

    return HttpResponse("Error: Unable to resend OTP. Please check your credentials.")


def forgot_psw(request):
    if request.method == "POST":
        mob_no = request.POST.get("mob_no")
        user = None
        try:
            admin_profile = Admin.objects.get(contact_no=mob_no)
            user = admin_profile.users
            request.session["admin_profile"] = admin_profile.id

        except Admin.DoesNotExist:
            pass

        try:
            employee_profile = Employee.objects.get(contact_no=mob_no)
            user = employee_profile.users
        except Employee.DoesNotExist:
            pass

        try:
            agent_profile = Agent.objects.get(contact_no=mob_no)
            user = agent_profile.users
        except Agent.DoesNotExist:
            pass

        try:
            outsourceagent_profile = OutSourcingAgent.objects.get(contact_no=mob_no)
            user = outsourceagent_profile.users
        except OutSourcingAgent.DoesNotExist:
            pass

        if user is not None:
            request.session["user_id"] = user.id

            random_number = random.randint(0, 999)
            forgetsend_otp = str(random_number).zfill(4)
            request.session["forgotsendotp"] = forgetsend_otp

            url = "http://sms.txly.in/vb/apikey.php"
            payload = {
                "apikey": "lbwUbocDLNFjenpa",
                "senderid": "SKTRAL",
                "templateid": "1007338024565017323",
                "number": mob_no,
                "message": f"Use this OTP {forgetsend_otp} to login to your. theskytrails account",
            }
            response = requests.post(url, data=payload)

            return redirect("forget_otp")

        else:
            messages.error(request, "Mobile number does not match any user.")

    return render(request, "Login/forgot_psw.html")

    # return render(request, "Authentication/forgot_psw.html")


def forget_otp(request):
    sendotp = request.session.get(
        "forgotsendotp", "Default value if key does not exist"
    )
    print("sendd otp", sendotp)
    if request.method == "POST":
        num1 = request.POST.get("num1")
        num2 = request.POST.get("num2")
        num3 = request.POST.get("num3")
        num4 = request.POST.get("num4")
        num5 = request.POST.get("num5")
        num6 = request.POST.get("num6")
        submitted_otp = num1 + num2 + num3 + num4 + num5 + num6
        # submitted_otp = request.POST.get("submitted_otp")
        if submitted_otp == sendotp:
            return redirect("reset_psw")
        else:
            messages.error(request, "OTP not matched..")

    return render(request, "Login/Forgot_otp_verify.html")


def reset_psw(request):
    user_id = request.session.get("user_id", "Default value if key does not exist")

    if request.method == "POST":
        new_psw = request.POST.get("new_psw")
        confirm_psw = request.POST.get("confirm_psw")

        if new_psw == confirm_psw:
            user_instance = CustomUser.objects.get(id=user_id)

            try:
                # Use set_password to properly hash and save the password
                # print("Before setting password:", user_instance.password)
                user_instance.set_password(confirm_psw)
                # print("After setting password:", user_instance.password)
                user_instance.save()

                messages.success(request, "Password Reset Successfully....")

                return redirect("login")
            except Exception as e:
                messages.error(request, f"An error occurred: {e}")

        else:
            messages.error(request, "Password Not Match")

    return render(request, "Login/change_psw.html")


def Error404(request, exception):
    return render(request, "Admin/404.html")


def chats(request):
    user = request.user
    user_type = user.user_type

    if user_type == "2":
        chat_groups = ChatGroup.objects.all()
    else:
        chat_groups = user.chat_member.all()

    if user_type == "2":
        base_template = "Admin/Base/base.html"
    elif user_type == "3":
        base_template = "Employee/Base/base.html"
    else:
        base_template = "Agent/Base/base.html"

    context = {
        "base_template": base_template,
        "groups": chat_groups,
        "user_type": user_type,
    }
    return render(request, "chat/chat2.html", context)


def get_group_chat_messages(request):
    group_id = request.GET.get("group_id")
    user = request.user

    chat_group = ChatGroup.objects.get(id=group_id)

    chat = ChatMessage.objects.filter(group=chat_group)
    group_name = chat_group.group_name

    context = {
        "chat_group": chat_group,
        "chat": chat,
        "user": user,
        "group_name": group_name,
    }

    chat_content = loader.render_to_string("chat/group_chat_content.html", context)
    return HttpResponse(chat_content)
