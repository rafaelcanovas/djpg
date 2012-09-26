from django.dispatch import Signal
from .codes import codes

notification_received = Signal(providing_args=['notification'])
transaction_received = Signal(providing_args=['transaction'])

transaction_waiting = Signal()
transaction_analysis = Signal()
transaction_paid = Signal()
transaction_available = Signal()
transaction_dispute = Signal()
transaction_returned = Signal()
transaction_canceled = Signal()
transaction_unknown = Signal()


def dispatch_transaction(sender, **kwargs):
	transaction = kwargs.pop('transaction')
	status = int(transaction['status'])

	signals = {
		codes.waiting: transaction_waiting,
		codes.analysis: transaction_analysis,
		codes.paid: transaction_paid,
		codes.available: transaction_available,
		codes.dispute: transaction_dispute,
		codes.returned: transaction_returned,
		codes.canceled: transaction_canceled
	}

	signals.get(status, transaction_unknown).send(
		sender=None,
		transaction=transaction)

transaction_received.connect(dispatch_transaction)
