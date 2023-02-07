from databases.models import ClientAdmin
import string
def get_username_from_request(request):
    user  = ClientAdmin.objects.get(user=request.user)
    return string.capwords(str(user.name))