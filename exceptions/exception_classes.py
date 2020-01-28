



class NoDataFound(Exception):
    """ Exception if api couldn't find any data.
    """
    def __init__(self, message):
        self.message = message

class NoLocation(Exception):
    """ Location is not entered correctly.
    """
    def __init__(self, message):
        self.message = message
