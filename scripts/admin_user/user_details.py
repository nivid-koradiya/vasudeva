from databases.models import ClientAdmin
from django.contrib.auth.models import User
import string
def get_username_from_request(request):
    user = User.objects.get(username = request.user)
    return string.capwords(str(user.first_name))

def get_client_name_from_request(request):
    user = User.objects.get(username = request.user)
    cleint_admin = ClientAdmin.objects.get(user = user)
    name = ClientAdmin.name
    return string.capwords(name)
