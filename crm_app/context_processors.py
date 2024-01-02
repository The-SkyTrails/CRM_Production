from .models import FAQ


def faq_count(request):
    if request.user.is_authenticated:
        count = FAQ.objects.all().count()
    else:
        count = 0
    return {'faq_count': count}


