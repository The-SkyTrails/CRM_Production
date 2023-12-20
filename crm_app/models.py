from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
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

type = [
    ('Outsourcing partner','Outsourcing partner'),
    ('Agent','Agent'),

]

status = [
    ('Pending','Pending'),
    ('InReview','InReview'),
    ('Approved','Approved'),
    ('Reject','Reject'),
]

Department_Choices = [
    ("Presales/Assesment", "Presales/Assesment"),
    ("Sales", "Sales"),
    ("Documentation","Documentation"),
    ("Visa Team","Visa Team"),
    ("HR", "HR"),
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

class Admin(models.Model):
    users = models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    department = models.CharField(max_length=50)
    contact_no = models.CharField(max_length=10,unique=True)

    def __str__(self):
        return self.users.first_name

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
    
    
class LoginLog(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    platform = models.CharField(max_length=200,default="Web")
    ip_address = models.GenericIPAddressField()
    login_datetime = models.DateTimeField(auto_now_add=True)
    # date = models.DateField()

    def save(self, *args, **kwargs):
        # Format the date and time as "13-Sep-2023 01:56 PM"
        formatted_datetime = self.login_datetime.strftime('%d-%b-%Y %I:%M %p')
        self.login_datetime_formatted = formatted_datetime
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.login_datetime}"
    
    
class Employee(models.Model):
    users = models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    branch = models.ForeignKey(Branch,on_delete=models.SET_NULL,null=True,blank=True)
    department = models.CharField(max_length=20,null=True, blank=True,choices=Department_Choices)
    group = models.ForeignKey(Group,on_delete=models.SET_NULL,null=True,blank=True)
    contact_no = models.CharField(max_length=20,null=True,blank=True)
    country = models.CharField(max_length=50,null=True,blank=True)
    state = models.CharField(max_length=50,null=True,blank=True)
    City = models.CharField(max_length=50,null=True,blank=True)
    Address = models.TextField(null=True,blank=True)
    zipcode = models.CharField(max_length=100,null=True,blank=True)
    file = models.FileField(upload_to="media/Employee/profile_pic/",null=True,blank=True)
    created = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        # Check if a group is provided when saving the employee
        if self.group:
            # Add the employee to the group
            self.group.group_member.add(self.users)
        super(Employee, self).save(*args, **kwargs)
        
    def __str__(self):
        return self.users.username
    

class Agent(models.Model):
    users = models.OneToOneField(CustomUser,on_delete=models.CASCADE)  
    type = models.CharField(max_length=255)
    contact_no = models.CharField(max_length=20)
    country = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    City = models.CharField(max_length=50)
    Address = models.TextField()
    zipcode = models.CharField(max_length=100)
    dob = models.DateField(null=True,blank=True)
    gender = models.CharField(max_length=10)
    marital_status = models.CharField(max_length=10,null=True,blank=True)
    status = models.CharField(max_length=255,choices=status,default='Pending')
    activeinactive=models.BooleanField(default=True,null=True,blank=True)
    profile_pic = models.ImageField(upload_to="media/Agent/Profile Pic/",null=True,blank=True)
    assign_employee = models.ForeignKey(Employee,on_delete=models.CASCADE,null=True,blank=True)

    organization_name = models.CharField(max_length=100,null=True,blank=True)
    business_type = models.CharField(max_length=100,null=True,blank=True)
    registration_number = models.CharField(max_length=100,null=True,blank=True)

    # ---------- Bank Information ---------------- 

    account_holder = models.CharField(max_length=100,null=True,blank=True)
    bank_name = models.CharField(max_length=100,null=True,blank=True)
    branch_name = models.CharField(max_length=100,null=True,blank=True)
    account_no = models.CharField(max_length=100,null=True,blank=True)
    ifsc_code = models.CharField(max_length=100,null=True,blank=True)
    last_updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    registeron = models.DateTimeField(auto_now_add=True, auto_now=False)
    registerdby = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='registered_agents')

    # -------------------------- kyc information ------------------ 

    adhar_card_front = models.FileField(upload_to="media/Agent/Kyc",null=True,blank=True)
    adhar_card_back = models.FileField(upload_to="media/Agent/Kyc",null=True,blank=True)
    pancard = models.FileField(upload_to="media/Agent/Kyc",null=True,blank=True)
    registration_certificate = models.FileField(upload_to="media/Agent/Kyc",null=True,blank=True)
    


class OutSourcingAgent(models.Model):
    
    
    users = models.OneToOneField(CustomUser,on_delete=models.CASCADE)  
    type = models.CharField(max_length=255)
    contact_no = models.CharField(max_length=20)
    country = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    City = models.CharField(max_length=50)
    Address = models.TextField()
    zipcode = models.CharField(max_length=100)
    dob = models.DateField(null=True,blank=True)
    gender = models.CharField(max_length=10)
    marital_status = models.CharField(max_length=10,null=True,blank=True)
    status = models.CharField(max_length=255,choices=status,default='Pending')
    activeinactive=models.BooleanField(default=True,null=True,blank=True)
    profile_pic = models.ImageField(upload_to="media/OutSourcing/Agent/Profile Pic/",null=True,blank=True)
    assign_employee = models.ForeignKey(Employee,on_delete=models.CASCADE,null=True,blank=True)

    organization_name = models.CharField(max_length=100,null=True,blank=True)
    business_type = models.CharField(max_length=100,null=True,blank=True)
    registration_number = models.CharField(max_length=100,null=True,blank=True)

    # ---------- Bank Information ---------------- 

    account_holder = models.CharField(max_length=100,null=True,blank=True)
    bank_name = models.CharField(max_length=100,null=True,blank=True)
    branch_name = models.CharField(max_length=100,null=True,blank=True)
    account_no = models.CharField(max_length=100,null=True,blank=True)
    ifsc_code = models.CharField(max_length=100,null=True,blank=True)
    last_updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    registeron = models.DateTimeField(auto_now_add=True, auto_now=False)
    registerdby = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='registered_outsourcingagents')


    # -------------------------- kyc information ------------------ 

    adhar_card_front = models.FileField(upload_to="media/Agent/Kyc",null=True,blank=True)
    adhar_card_back = models.FileField(upload_to="media/Agent/Kyc",null=True,blank=True)
    pancard = models.FileField(upload_to="media/Agent/Kyc",null=True,blank=True)
    registration_certificate = models.FileField(upload_to="media/Agent/Kyc",null=True,blank=True)
    

@receiver(post_save,sender=CustomUser)
def create_admin_profile(sender,instance,created, **kwargs):
    # if instance.user_type==''
    if created:
        if instance.user_type == '2':
            Admin.objects.create(users=instance, contact_no='')
        elif instance.user_type == '3':  # Check if the user type is 'ManPower'
            # branch = Branch.objects.get(id=1)
            Employee.objects.create(users=instance, contact_no='',zipcode='',file='')
    
        elif instance.user_type == '4':  # Check if the user type is 'ManPower'
            Agent.objects.create(users=instance, contact_no='',zipcode='',activeinactive='True',type='',profile_pic='')
    
        elif instance.user_type == '5':  # Check if the user type is 'ManPower'
            OutSourcingAgent.objects.create(users=instance, contact_no='',zipcode='',activeinactive='True',type='',profile_pic='')
    

@receiver(post_save,sender=CustomUser)
def save_user_profile(sender,instance, **kwargs):
    if instance.user_type=='2':
        instance.admin.save()
    if instance.user_type=='3':
        instance.employee.save()
    if instance.user_type=='4':
        instance.agent.save()
    if instance.user_type=='5':
        instance.outsourcingagent.save()