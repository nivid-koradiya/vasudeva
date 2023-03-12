import datetime
from databases.models import(
    Client,
    SurfaceUser,
    SurfaceUserAuthLog,
    
)
from .client import get_client_object_from_request
from zoneinfo import ZoneInfo
def create_surfaceuser(request):
    try:
        name = request.data['name']
        username = request.data['username']
        password = request.data['password']
        is_active = request.data['is_active']
        user =SurfaceUser()
        user.name = name
        user.username = username
        user.password = password
        user.client = get_client_object_from_request(request)
        user.is_active = is_active
        user.save()
        
        return {
            'id' : user.id,
            # 'username' : user.username,
            # 'name': user.name,
            'is_active' : user.is_active,
            'created_at' : user.created_at.astimezone(ZoneInfo('Asia/Kolkata'))
        }
    except: 
        return False
    
def get_surfaceuser(request):
    try:
        username =  request.GET.get('username')
        user = SurfaceUser.objects.get(username =username)
        return {
            'id' : user.username,
            'username' : user.username,
            'name' : user.name,
            'client' : user.client.organisation,
            'is_active' : user.is_active,
            'created_at' : user.created_at.astimezone(ZoneInfo('Asia/Kolkata')),
            
        }
    except:
        return False

def authenticate_surfaceuser(request):
    try:
        username = request.data['username']
        password = request.data['password']
        user = SurfaceUser.objects.get(username=username, password=password)
        return {
            "authenticated" : True,
            "timestamp" : datetime.datetime.now()
        }
    except:
        return False
    