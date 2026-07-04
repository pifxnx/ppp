class AppException(Exception):
    def __init__(self, message, status_code):
        self.message = message
        self.status_code = status_code


class NotFoundException(AppException):
    def __init__(self, recource, identifier):
        self.recource = recource
        self.identifier = identifier
        



