import logging
from django.contrib.auth.signals import user_login_failed
from django.dispatch import receiver

logger = logging.getLogger('authentication')

@receiver(user_login_failed)
def log_authentication_failure(sender, credentials, request, **kwargs):
    logger.warning(f"Failed authentication attempt. Username: {credentials.get('username')} from : {get_client_ip(request)}")

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
