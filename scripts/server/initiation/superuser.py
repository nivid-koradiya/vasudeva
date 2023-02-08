import os

import environ
from django.contrib.auth.models import User

from vasudeva.settings import BASE_DIR

env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR,'.env')) 

def initiate_superuser(auth):
    if auth == env('SU_KEY'):
        existing_user = User.objects.filter(username= str( env('SU_USER') ) )
        if len(existing_user)>0:
            return False
        try:
            user = User()
            user.is_superuser= True
            user.username = env('SU_USER')
            user.set_password(env('SU_PASS'))
            user.first_name = 'PREET'
            user.is_staff = True
            user.is_active = True
            user.save()
        except:
            return False
        return True
    else:
        return False