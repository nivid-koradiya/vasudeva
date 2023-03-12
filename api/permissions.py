from rest_framework import permissions
from databases.models import ApiKeys

class ApiKeyPermission(permissions.BasePermission):
    message='you are not welcome here!'
    def has_permission(self, request, view):
        try:
            token = request.headers.get('Authorization')
            # print(token)
            key = (ApiKeys.objects.filter(key_value = token.split(' ')[-1]))
            if len(key) == 1:
                return True
            else: 
                return False
        except:
            return False