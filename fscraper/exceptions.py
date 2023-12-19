class CodeNotFoundException(Exception):
    """Raised when the code was not listed"""

    def __init__(self, code, message):
        self.code = code
        self.message = message
