from manager import Reader, Manager

reader = Reader('in.txt')
manager = Manager(reader)

def saldo(manager, rows):
    price = float(rows[0])
    manager.modify_account(price)

manager.action('saldo', 2, saldo)
manager.process()