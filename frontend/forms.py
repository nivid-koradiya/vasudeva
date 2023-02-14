from captcha.fields import CaptchaField
from django import forms
from databases.models import client_mobile_validator
class AdminLoginForm(forms.Form):
    username = forms.CharField()
    password=  forms.CharField()
    captcha = CaptchaField(label='')
    

class AjaxNewClient(forms.Form):
    company  = forms.CharField(max_length=100, required=True)
    phone = forms.CharField(max_length=10,validators=[client_mobile_validator])
    # status = forms.BooleanField()