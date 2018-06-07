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
        notification_code = request.POST['notificationCode']
    except KeyError:
        return HttpResponseBadRequest()

    logger.info('Notification with type "%s" and code "%s" received'
                % (notification_type, notification_code))

    notification = Notification(notification_code, type=notification_type)
    notification_received.send(sender=None, notification=notification)

    data = notification.get_data()

    if data:
        if notification.type == 'transaction':
            try:
                transaction = data['transaction']
                transaction_received.send(sender=None, transaction=transaction)
            except KeyError:
                pass

    return HttpResponse()
