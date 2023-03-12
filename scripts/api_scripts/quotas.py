from databases.models import (
    Quota,
    Client,
    ApiKeys
)

def deduct_quota_request(request):
    try:
        token = request.headers.get('Authorization')
        client = ApiKeys.objects.get(key_value = token.split(' ')[-1]).client
        quota = Quota.objects.get(client = client)
        quota.quantity = quota.quantity - 1
        if quota.quantity < 1:
            return False
        else:
            quota.save()
            return True
    except:
        return False