from django.shortcuts import render


# Create your views here.
def visa_home(request):
    return render(request, "VisaPage/home.html")


def visa_details(request):
    return render(request, "VisaPage/Visa1.html")


def investvisa_details(request):
    return render(request, "VisaPage/Investvisa.html")


def studyvisa_details(request):
    return render(request, "VisaPage/Studyvisa.html")


def ssdc(request):
    return render(request, "VisaPage/ssdc.html")


def overseas(request):
    return render(request, "VisaPage/Overseas.html")


def overseas_all(request):
    return render(request, "VisaPage/overseasjobs2.html")


def overseas_details(request):
    return render(request, "VisaPage/overseasjob3.html")


def blog(request):
    return render(request, "VisaPage/Blogs1.html")


def blog_details(request):
    return render(request, "VisaPage/blog_details.html")


def immigrationblog(request):
    return render(request, "VisaPage/immigrationblog.html")


def aboutus(request):
    return render(request, "VisaPage/Aboutus.html")


def privacypolicy(request):
    return render(request, "VisaPage/Privacypolicy.html")


def antifraud(request):
    return render(request, "VisaPage/Antifruad.html")


def termscondition(request):
    return render(request, "VisaPage/Termscondition.html")


def refundcancellation(request):
    return render(request, "VisaPage/Refundcancelation.html")
