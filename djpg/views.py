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
