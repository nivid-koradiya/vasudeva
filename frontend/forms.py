from captcha.fields import CaptchaField
from django import forms

class AdminLoginForm(forms.Form):
    username = forms.CharField()
    password=  forms.CharField()
    captcha = CaptchaField(label='')