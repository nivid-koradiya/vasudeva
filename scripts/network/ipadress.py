from vasudeva.settings import LOG_IP
from databases.models import RequestLog as RL
def get_ip(request):
    if LOG_IP:
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        log = RL()
        log.ip_address = ip
        log.save()
    else:
        return