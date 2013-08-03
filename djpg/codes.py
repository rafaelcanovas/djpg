class CodesDict(object):
	def __init__(self, codes):
		self.__dict__.update(codes)

_codes = {
	'waiting': 1,
	'analysis': 2,
	'paid': 3,
	'available': 4,
	'dispute': 5,
	'returned': 6,
	'canceled': 7,
}

codes = CodesDict(_codes)
