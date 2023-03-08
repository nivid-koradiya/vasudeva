from databases.models import LoginLog
from django.contrib.auth.models import User
def admin_login_log(request,mode_of_login = 'browser'):
    try:
        log = LoginLog()
        log.user = User.objects.get(username = str(request.user))
        log.mode_of_login = mode_of_login
        log.status = True
        log.save()
        return True
    except :
        return Exception 
    
def admin_logout_log(request,mode_of_login = 'browser'):
    try:
        log = LoginLog()
        log.user = User.objects.get(username = str(request.user))
        log.mode_of_login = mode_of_login
        log.status = False
        log.save()
        return True
    except :
        return Exception 
    
def client_logout_log(request,mode_of_login = 'browser'):
    try:
        log = LoginLog()
        log.user = User.objects.get(username = str(request.user))
        log.mode_of_login = mode_of_login
        log.status = False
        log.save()
        return True
    except :
        return Exception 

def client_login_log(request,mode_of_login = 'browser'):
    try:
        log = LoginLog()
        log.user = User.objects.get(username = str(request.user))
        log.mode_of_login = mode_of_login
        log.status = True
        log.save()
        return True
    except :
        return Exception 