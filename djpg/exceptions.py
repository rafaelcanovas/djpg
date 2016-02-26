class PagSeguroUnauthorizedException(Exception):
    pass


class PagSeguroInvalidRequestException(Exception):
    def __init__(self, code, msg):
        self.code = code
        self.msg = msg

    def __str__(self):
        return '[{}] {}'.format(self.code, self.msg)
