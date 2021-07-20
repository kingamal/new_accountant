
class NotEnoughDataException(Exception):
    pass

class Manager():
    def __init__(self, path):
        self.pathfile = path
        self.file = open(path)
        self.history = []
        self.account = 0
        self.stock = {}
        pass

    def getline(self, count=1):
        countlist = []
        for i in range(count):
            readline = self.file.readline()
            if not readline:
                raise NotEnoughDataException()
            countlist.append(readline)
        return countlist
