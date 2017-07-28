import logging
logger = logging.getLogger('djpg')

from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseBadRequest

from .models import Notification
from .signals import notification_received, transaction_received


@require_POST
@csrf_exempt
def notifications(request):
    try:
        notification_type = request.POST['notificationType']
    except KeyError:
        logger.info('Notification received without "notificationType"')
        return HttpResponseBadRequest()

    try:
        notification_code = request.POST['notificationCode']
    except KeyError:
        logger.info('Notification received without "notificationCode"')
        return HttpResponseBadRequest()

    logger.info('Notification with type "%s" and code "%s" received'
                % (notification_type, notification_code))

    notification = Notification(type=notification_type, code=notification_code)
    notification_received.send(sender=None, notification=notification)

    content = notification.fetch_content()
    if content:
        if notification.type == 'transaction':
            try:
                transaction = content['transaction']
                transaction_received.send(sender=None, transaction=transaction)
            except KeyError:
                pass

    return HttpResponse()
