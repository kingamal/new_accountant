import sys
from manager import Reader, Manager

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

manager.process()
manager.execute_action(sys.argv[1:])
manager.writeline('out.txt')

