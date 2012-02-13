# Small custom errors

class LocateError(Exception):
    def __init__(self, path):
        self.path = path

    def __str__(self):
        return 'Could not locate {}'.format(self.path)
