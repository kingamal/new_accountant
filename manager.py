
class NotEnoughDataException(Exception):
    pass


class NotEnoughMoneyException(Exception):
    pass


class NotEnoughStockException(Exception):
    pass


class NoActionException(Exception):
    pass


class NotEnoughParametersException(Exception):
    pass


class Manager:
    def __init__(self, reader):
        self.reader = reader
        self.history = []
        self.account = 0
        self.stock = {}
        self.actions = {}

    def modify_account(self, value):
        if self.account + value < 0:
            raise NotEnoughMoneyException()
        self.account += value

    def add_history(self, row):
        self.history.append(row)
        return self.history

    def modify_stock(self, item, qty):
        if item not in self.stock:
            self.stock[item] = 0
        if self.stock[item] + qty < 0:
            raise NotEnoughStockException()
        self.stock[item] += qty

    def action(self, name, parameters=-1):
        def action_in(callback):
            self.actions[name] = (parameters, callback)
        return action_in

    def process(self):
        while True:
            action = self.reader.getline()[0]
            if action == 'stop':
                break
            if action not in self.actions:
                raise NoActionException()
            parameters, callback = self.actions[action]
            rows = self.reader.getline(parameters)
            if callback(self, rows):
                self.add_history([action] + rows)

    def writeline(self, file_out):
        with open(file_out, 'w') as f:
            for wartosc in self.history:
                for dane in wartosc:
                    f.write(str(dane) + '\n')
            f.write('stop')

    def execute_action(self, param):
        action = param[0]
        parameters, callback = self.actions[action]
        if parameters >= 0 and len(param) - 1 != parameters:
            raise NotEnoughParametersException()
        if callback(self, param[1:]):
            self.add_history(param)


class Reader:
    def __init__(self, path):
        self.pathfile = path
        self.file = open(path)

    def getline(self, count=1):
        countlist = []
        for i in range(count):
            readline = self.file.readline()
            if not readline:
                raise NotEnoughDataException("za malo danych w pliku")
            countlist.append(readline.strip())
        return countlist

