from django.db import models
import uuid
import re
import datetime as dt
from django.forms import ValidationError
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
import secrets as se
# Create your models here.


# GENERAL FUNCTIONS
def generate_uuid():
    return str(uuid.uuid4()) #RETURN UUID v4 in string format






# Logging Functions:
# Logging Models
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
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    status = models.BooleanField()
    class Meta:
        verbose_name = ("Login log")
        verbose_name_plural = ("Login logs")
        db_table = "log_login"
        
    def __str__(self):
        return self.id







# ORG/CLIENT USER FUNCTIONS
def client_mobile_validator(mobile):
    mobile= str(mobile)
    if mobile.isnumeric() and len(mobile)==10:
        return True
    else:
        raise ValidationError("Mobile No is not valid")
        
# ORG/CLIENT USER MODELS
class Client(models.Model):
    id = models.CharField(default=generate_uuid, primary_key=True,max_length=42)
    organisation = models.CharField(max_length=255)
    mobile = models.CharField(max_length=10,validators=[client_mobile_validator])
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


# Client Admin:
class ClientAdmin(models.Model):
    id = models.CharField(default=generate_uuid, primary_key=True,max_length=42)
    name = models.CharField(max_length=125,null=False,default='default')
    username = models.CharField(max_length=64,validators=[validate_username],null=False)
    email = models.EmailField(max_length=254,null=False,default='defaultmail@mail.com')
    timestamp = models.DateTimeField(auto_now_add=True)
    client = models.ForeignKey('Client',on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    class Meta:
        verbose_name = ("ClientAdmin")
        verbose_name_plural = ("ClientAdmins")
        db_table= "client_admin"
    def __str__(self):
        return self.username


# Quotas Functions:
# Quotas MODEL:
class Quota(models.Model):
    id = models.CharField(default=generate_uuid, primary_key=True,max_length=42)
    client = models.OneToOneField(Client, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    mail = models.IntegerField()
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = ("Quota")
        verbose_name_plural = ("Quotas")
        db_table = 'quotas'

    def __str__(self):
        return str(self.client)
    
    
# Surface user functions
# Surface user Model
class SurfaceUser(models.Model):
    id = models.CharField(default=generate_uuid, primary_key=True,max_length=42)
    name = models.CharField(max_length=50)
    username = models.CharField(default='user',max_length=64,unique=True)
    password = models.CharField(default='',max_length=300)
    client = models.ForeignKey(Client,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)
    desc = models.CharField(max_length=10000)
    
    
# Surface User Auth Log functions
# Surface User Auth Log
class SurfaceUserAuthLog(models.Model):
    id =  models.CharField(default=generate_uuid, primary_key=True,max_length=42)
    user = models.ForeignKey(SurfaceUser,on_delete=models.CASCADE, null=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    
# API KEY MODEL FUNCTIONS
def generate_api_key():
    api_key = uuid.uuid4().hex
    return api_key
# API KEY MODEL 
class ApiKeys(models.Model):
    id =  models.CharField(default=generate_uuid, primary_key=True,max_length=42)
    key_value = models.CharField(max_length=64,default=generate_api_key)
    client = models.ForeignKey(Client,on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    

    
    
def generate_verification_token():
    return str(uuid.uuid4().hex)
class ClientVerificationToken(models.Model):
    id =  models.CharField(default=generate_uuid, primary_key=True,max_length=42)
    token = models.CharField(max_length=100,default=generate_verification_token,unique=True)
    timestamp = models.DateTimeField(auto_now_add=True,null=False)
    client = models.ForeignKey(Client,on_delete=models.CASCADE)
    
class RequestLog(models.Model):
    id =  models.CharField(default=generate_uuid, primary_key=True,max_length=42)
    ip_address = models.CharField(max_length=32,null=False)
    path = models.CharField(max_length=1000,null=False)
    timestamp  = models.DateTimeField(auto_now_add=True,null=False,editable=False)
    method = models.CharField(null=False,max_length=8)
    user = models.CharField(null=False,max_length=100)

    class Meta:
        verbose_name = ("Request Log")
        verbose_name_plural = ("Request Logs")
        db_table = 'request_log'
        
    def __str__(self):
        return str(self.timestamp.tzinfo)
    
class RechargeRate(models.Model):
    id =  models.CharField(default=generate_uuid, primary_key=True,max_length=42)
    request_rate = models.IntegerField()
    mail_rate = models.IntegerField()
    timestamp  = models.DateTimeField(auto_now_add=True,null=False,editable=False)

    class Meta:
        verbose_name = ("Recharge Rate")
        verbose_name_plural = ("Recharge Rates")
        db_table = 'recharge_rate'
        
    def __str__(self):
        return str(self.timestamp)
    
class PaymentsLog(models.Model):
    id =  models.CharField(default=generate_uuid, primary_key=True,max_length=42)
    payment_id =  models.CharField(unique=True,max_length=100)
    order_id =  models.CharField(unique=True,max_length=100)
    timestamp  = models.DateTimeField(auto_now_add=True,null=False,editable=False)
    client = models.ForeignKey(Client,on_delete=models.CASCADE)
    rate = models.ForeignKey(RechargeRate,on_delete=models.CASCADE)
    amount =models.IntegerField()
    class Meta:
        verbose_name = ("Payment Log")
        verbose_name_plural = ("Payment Logs")
        db_table = 'payment_log'
        
    def __str__(self):
        return str(self.timestamp)

    
class LogApiRequests(models.Model):
    id =  models.CharField(default=generate_uuid, primary_key=True,max_length=42)
    key_used = models.CharField(max_length=100)
    ip_address = models.CharField(max_length=32,null=False)
    path = models.CharField(max_length=1000,null=False)
    timestamp  = models.DateTimeField(auto_now_add=True,null=False,editable=False)
    method = models.CharField(null=False,max_length=8)
    
    class Meta:
        verbose_name = ("API Request Log")
        verbose_name_plural = ("API Request Logs")
        db_table = 'api_request_log'
        
    def __str__(self):
        return str(self.id)