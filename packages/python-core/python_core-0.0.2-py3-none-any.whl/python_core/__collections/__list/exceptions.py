

class ListException(Exception):
    def __init__(self, message=""):
        self.message = message


class EmptyListError(ListException):
    pass