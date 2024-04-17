"""Generic errors"""
class EntityException(Exception):
    """Entity Exception"""
    def __init__(self, message: str):
        self.message = message


class Unauthenticated(Exception):
    """Unauthenticated"""
    def __init__(self, message: str):
        self.message = message


class UnauthenticatedForbidden(Exception):
    """Unauthenticated Forbidden"""
    def __init__(self, message: str):
        self.message = message


class Unauthorized(Exception):
    """Unauthorized"""
    def __init__(self):
        pass

class FormParseException(Exception):
    """Form Parse Exception"""
    def __init__(self, message):
        self.message = message
