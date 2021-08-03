from flask import Flask, render_template, request, redirect
from accountant import manager, reader

app = Flask(__name__)

def read_in():
    content = reader.getline()
    return content

def write_out():
    manager.writeline('in.txt')

@app.route('/', methods=["GET", "POST"])
def homepage():
    stock = manager.stock.items()
    account = manager.account
    errors = {}
    if request.method == "POST":
        action = request.form.get('action')
        if action not in ['buy', 'sell', 'balance']:
            errors['action'] = 'No action'
        if action == 'buy':
            manager.execute_action(['zakup', request.form['product'], request.form['unit_price'], request.form['qty']])
        if action == 'sell':
            manager.execute_action(['sprzedaz', request.form['product'], request.form['unit_price'], request.form['qty']])
        if not errors:
            write_out()
            return redirect('/')
    return render_template('index.html', stock=stock, account=account, errors=errors)

@app.route('/history/')
def history():
    history = manager.history
    return render_template('history.html', history=history)