class Robot:

    def __init__(self):

        self.name = self.__class__.__name__[:-5].lower()
