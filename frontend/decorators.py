from vasudeva.settings import LOG_IP
from databases.models import RequestLog as RL
def log_ip_address(function):
    def wrap(request, *args, **kwargs):
        if LOG_IP:
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0]
            else:
                ip = request.META.get('REMOTE_ADDR')
            log = RL()
            log.ip_address = ip
            log.path = request.get_full_path()
            log.method = request.method
            log.user = request.user
            log.save()
            return function(request, *args, **kwargs)
        else:
            raise Exception("IP Could Not be verified!")
    return wrap
