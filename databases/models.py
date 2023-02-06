from django.db import models
import uuid
import re
import datetime as dt
from django.forms import ValidationError
from django.contrib.auth.hashers import make_password
# Create your models here.


#GENERAL FUNCTIONS
def generate_uuid():
    return str(uuid.uuid4()) #RETURN UUID v4 in string format






#logging Functions:
#Logging Models
class LoginLog(models.Model):
    id =  models.CharField(default=generate_uuid, primary_key=True,max_length=42)
    #TODO Add user field here
    timestamp = models.DateTimeField(auto_now_add=True)
    #choices for Mode of login
    mode_of_login_choices = (
        ('browser','browser'),
        ('other','other'),
        # ('',''),
    )
    mode_of_login = models.CharField(max_length=100,choices=mode_of_login_choices,default='browser')
    class Meta:
        verbose_name = ("login_log")
        verbose_name_plural = ("login_logs")
        db_table = "log_login"
        
    def __str__(self):
        return self.id





#ORG/CLIENT USER FUNCTIONS
def client_mobile_validator(mobile):
    mobile= str(mobile)
    if mobile.isnumeric() and len(mobile)==10:
        return True
    else:
        raise ValidationError("Mobile No is not valid")
        
#ORG/CLIENT USER MODELS
class Client(models.Model):
    id = models.CharField(default=generate_uuid, primary_key=True,max_length=42)
    organisation = models.CharField(max_length=255)
    # admin = models.CharField() #TODO #ADD ADMIN TABLE USER HERE
    mobile = models.CharField(max_length=10,validators=[])
    timestamp = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=False)

    class Meta:
        verbose_name = ("client")
        verbose_name_plural = ("clients")
        db_table = "clients"
        
    def __str__(self):
        return self.organisation



# Client Admin functions
def validate_username(username):
    username_len = len(username)
    username = str(username)
    if username_len >=8 and username_len<33 and re.match(r'^\w+$', username):
        return True
    else:
        raise ValidationError("Username is not Valid")

def generate_default_password_hash():
    hashed_password = ""
    hashed_password = make_password('admin')
    return hashed_password
# Client Admin:
class ClientAdmin(models.Model):
    id = models.CharField(default=generate_uuid, primary_key=True,max_length=42)
    name = models.CharField(max_length=125,null=False,default='default')
    username = models.CharField(max_length=64,validators=[validate_username],null=False)
    email = models.EmailField(max_length=254,null=False,default='defaultmail@mail.com')
    timestamp = models.DateTimeField(auto_now_add=True)
    password = models.CharField(max_length=1280,null=False,default=generate_default_password_hash)
    client = models.ForeignKey('Client',on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = ("ClientAdmin")
        verbose_name_plural = ("ClientAdmins")
        db_table= "client_admin"
    def __str__(self):
        return self.username



#Quotas Functions:
# Quotas MODEL:
class Quota(models.Model):
    id = models.CharField(default=generate_uuid, primary_key=True,max_length=42)
    client = models.OneToOneField("databases.Client", on_delete=models.CASCADE)
    quantity = models.IntegerField()
    last_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = ("Quota")
        verbose_name_plural = ("Quotas")
        db_table = 'quotas'
        
    def __str__(self):
        return self.client

