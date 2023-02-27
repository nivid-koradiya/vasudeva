from captcha.fields import CaptchaField
from django import forms
from databases.models import client_mobile_validator, validate_username

def passwordvalidator(password):
    password = str(password)
    if len(password) > 8 :
        return True
    else:
        return False

class AdminLoginForm(forms.Form):
    username = forms.CharField()
    password=  forms.CharField()
    captcha = CaptchaField(label='')

class AjaxNewClient(forms.Form):
    company  = forms.CharField(max_length=100, required=True)
    phone = forms.CharField(max_length=10,validators=[client_mobile_validator])

class AjaxNewClientAdmin(forms.Form):
    username  = forms.CharField(max_length=100, required=True, validators=[validate_username])
    name  = forms.CharField(max_length=100, required=True)
    password  = forms.CharField(max_length=100, required=True,validators=[passwordvalidator])
    email = forms.EmailField()