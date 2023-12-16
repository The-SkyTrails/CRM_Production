from django.db import models
from django.contrib.auth.models import AbstractUser
from django_countries.fields import CountryField

# Create your models here.


class CustomUser(AbstractUser):
    user_type_data = (
        ("1", "HOD"),
        ("2", "Admin"),
        ("3", "Employee"),
        ("4", "Agent"),
        ("5", "Out Sourcing Agent"),
        ("6", "Customer"),
    )
    user_type = models.CharField(default="1", choices=user_type_data, max_length=10)
    is_logged_in = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class VisaCountry(models.Model):
    country = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now=True)
    lastupdated_by = models.CharField(max_length=100, null=True, blank=True)
    last_updated_on = models.DateTimeField(auto_now=True)

    def clean(self):
        self.country = self.country.capitalize()

    def __str__(self):
        return str(self.country)

    class Meta:
        db_table = "VisaCountry"
