from manager import Reader, Manager, NotEnoughDataException

reader = Reader('in.txt')
manager = Manager(reader)

@manager.action("saldo", 2)
def saldo(manager, rows):
    price = float(rows[0])
    manager.modify_account(price)


@manager.action("zakup", 3)
def zakup(manager, rows):
    name = rows[0]
    price = float(rows[1])
    qty = float(rows[2])
    manager.modify_account(-price*qty)
    manager.modify_stock(name, qty)

@manager.action("sprzedaz", 3)
def sprzedaz(manager, rows):
    name = rows[0]
    price = float(rows[1])
    qty = float(rows[2])
    manager.modify_account(price*qty)
    manager.modify_stock(name, qty)

@manager.action("konto")
def stan_konta(manager):
    print(manager.account)

@manager.action("magazyn")
def magazyn(manager):
    for product in manager.stock:
        if product in manager.stock:
            storage = manager.stock[product]
        else:
            storage = 0

@manager.action("przeglad")
def przeglad(manager, 2):
    for dictionary in magazyn.history[int(poczatek):int(koniec) + 1]: #argv
        data = dictionary.values()
        for sth in data:
            print(sth)

try:
   manager.process()
except NotEnoughDataException as exc:
    print(exc)

