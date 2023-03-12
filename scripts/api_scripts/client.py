from databases.models import (
    ApiKeys
)

def get_client_object_from_request(request):
    try:
        token = request.headers.get('Authorization')
        client = ApiKeys.objects.get(key_value = token.split(' ')[-1]).client
        return client
    except:
        return False