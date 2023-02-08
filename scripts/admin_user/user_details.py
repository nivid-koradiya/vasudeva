from databases.models import ClientAdmin
from django.contrib.auth.models import User
import string
def get_username_from_request(request):
    user = User.objects.get(username = request.user)
    return string.capwords(str(user.first_name))