from django.db import models
from django.contrib.auth.models import AbstractUser
from django_countries.fields import CountryField

BRANCH_SOURCES = [
    ('COCO','Company Owned Company Operated'),
    ('COFO','Company Owned Franchise Operated'),
    ('FOCO','Franchise Owned Company Operated'),
    ('FOFO','Franchise Owned Franchise Operated'),
]

COURIER_STATUS = [
    ('Pick','Pick'),
    ('In Transit','In Transit'),
    ('Receive','Receive')
]


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

    def __str__(self):
        return str(self.country)

    class Meta:
        db_table = "VisaCountry"
        

class VisaCategory(models.Model):
    visa_country_id = models.ForeignKey(VisaCountry,on_delete=models.CASCADE)    
    category = models.CharField(max_length=100)
    subcategory = models.CharField(max_length=100)
    lastupdated_by = models.CharField(max_length=100,null=True,blank=True)
    last_updated_on = models.DateTimeField(auto_now=True)
    

    class Meta:
        db_table = "VisaCategory"
        

    def __str__(self):
        return f"{self.category} - {self.subcategory}"
    
class DocumentCategory(models.Model):
    Document_category = models.CharField(max_length=200)
    lastupdated_by = models.CharField(max_length=100,null=True,blank=True)
    last_updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.Document_category
    
    
class Document(models.Model):
    document_name = models.CharField(max_length=255)
    document_category = models.ForeignKey(DocumentCategory, on_delete=models.CASCADE)
    document_size = models.FloatField()
    lastupdated_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True,blank=True)
    last_updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.document_name
    
    
class CaseCategoryDocument(models.Model):
    country = models.OneToOneField(VisaCountry,on_delete=models.CASCADE)
    category = models.ForeignKey(VisaCategory,on_delete=models.CASCADE,related_name='case_category')
    # subcategory = models.ForeignKey(VisaCategory,on_delete=models.CASCADE,related_name='case_subcategory')
    document = models.ManyToManyField(Document, related_name='document')
    last_updated_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    last_updated_on = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.country} - {self.category}"
    
class Branch(models.Model):
    branch_name = models.CharField(max_length=20)
    branch_source = models.CharField(max_length=50,choices=BRANCH_SOURCES)
    last_updated_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    last_updated_on = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.branch_name


class Group(models.Model):
    group_name = models.CharField(max_length=100, unique=True)
    group_member = models.ManyToManyField(CustomUser, related_name='groups_member')
    create_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.group_name 
    
    
class CourierAddress(models.Model):
    company_name = models.CharField(max_length=200)
    address = models.CharField(max_length=200,blank=True, null=True)
    landmark = models.CharField(max_length=200,blank=True, null=True)
    city = models.CharField(max_length=200,blank=True, null=True)
    state = models.CharField(max_length=200,blank=True, null=True)
    zipcode = models.IntegerField()
    docker_no = models.CharField(max_length=100)
    sender_no = models.CharField(max_length=15,blank=True, null=True)
    receiver_no = models.CharField(max_length=15,blank=True, null=True)
    courier_no = models.CharField(max_length=15,blank=True, null=True)
    receiver_address = models.CharField(max_length=150)
    sender_address = models.CharField(max_length=150,blank=True, null=True)
    status = models.CharField(max_length=50,choices=COURIER_STATUS)
    lastupdated_by = models.CharField(max_length=100,null=True,blank=True)
    last_updated_on = models.DateTimeField(auto_now=True)