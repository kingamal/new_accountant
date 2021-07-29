import sys
from manager import Reader, Manager, NotEnoughDataException

reader = Reader('in.txt')
manager = Manager(reader)

@manager.action("saldo", 2)
def saldo(manager, rows):
    price = float(rows[0])
    manager.modify_account(price)
    return True

@manager.action("zakup", 3)
def zakup(manager, rows):
    name = rows[0]
    price = float(rows[1])
    qty = float(rows[2])
    manager.modify_account(-price*qty)
    manager.modify_stock(name, qty)
    return True

@manager.action("sprzedaz", 3)
def sprzedaz(manager, rows):
    name = rows[0]
    price = float(rows[1])
    qty = float(rows[2])
    manager.modify_account(price*qty)
    manager.modify_stock(name, qty)
    return True

@manager.action('konto', 0)
def konto(manager, rows):
    print(manager.account)
    return False

@manager.action('magazyn')
def magazyn(manager, rows):
    products = rows[0:]
    for product in products:
        if product in manager.stock:
            stock = manager.stock[product]
        else:
            stock = 0
        print(product + ': ' + str(stock))

@manager.action('przeglad', 2)
def przeglad(self, rows):
    for dictionary in manager.history[int(rows[0]):int(rows[1])+1]:
        for value in dictionary:
            print((str(value)))
    print('stop')


try:
    manager.process()
except NotEnoughDataException as exc:
    print(exc)
#manager.execute_action(sys.argv[1:])
manager.writeline('out.txt')

