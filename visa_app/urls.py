from django.urls import path, include

from .views import *

urlpatterns = [
    path("", visa_home, name="visa_home"),
    path("visa/", visa_details, name="visa_details"),
    path("investvisa/", investvisa_details, name="investvisa_details"),
    path("studyvisa/", studyvisa_details, name="studyvisa_details"),
    path("ssdc/", ssdc, name="ssdc"),
    path("overseas/", overseas, name="overseas"),
    path("overseas_all/", overseas_all, name="overseas_all"),
    path("overseas_details/", overseas_details, name="overseas_details"),
    path("blog/", blog, name="blog"),
    path("blog_details/", blog_details, name="blog_details"),
    path("immigrationblog/", immigrationblog, name="immigrationblog"),
    path("aboutus/", aboutus, name="aboutus"),
    path("privacypolicy/", privacypolicy, name="privacypolicy"),
    path("antifraud/", antifraud, name="antifraud"),
    path("termscondition/", termscondition, name="termscondition"),
    path("refundcancellation/", refundcancellation, name="refundcancellation"),
]
