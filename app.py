from flask import Flask, render_template, request, redirect
from accountant import manager, reader
from flask_sqlalchemy import SQLAlchemy
from flask_alembic import Alembic

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

db = SQLAlchemy(app)


class History(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    what_action = db.Column(db.Integer, unique=False)
    # action = db.Column(db.Integer, unique=False) dopisac reszte


class Actions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    what_action = db.Column(db.String(32), unique=True)


class Stock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product = db.Column(db.String(64), unique=True)
    qty = db.Column(db.Integer, unique=False)
#
#
# db.create_all()
# alembic = Alembic(app)
# alembic.init_app(app)

# app_1 = Balance(value=1000000, comment='wplata poczatkowa')
# app_2 = Balance(value=-140000, comment='zus')
#
# db.session.add(app_1)
# db.session.add(app_2)
# db.session.commit()

# app_1 = Actions(what_action='saldo')
# app_2 = Actions(what_action='sprzedaz')
# app_3 = Actions(what_action='zakup')
#
# db.session.add(app_1)
# db.session.add(app_2)
# db.session.add(app_3)
# db.session.commit()


def read_in():
    content = reader.getline()
    return content

@app.route('/', methods=["GET", "POST"])
def homepage():
    stock = manager.stock.items()
    account = manager.account
    errors = {}
    if request.method == "POST":
        action = request.form.get('action')
        if action not in ['buy', 'sell', 'balance']:
            errors['action'] = 'Choose an action!'
        if action == 'buy':
            manager.execute_action(['zakup', request.form['product'], request.form['unit_price'], request.form['qty']])
        if action == 'sell':
            manager.execute_action(['sprzedaz', request.form['product'], request.form['unit_price'], request.form['qty']])
        if action == 'balance':
            manager.execute_action(['saldo', request.form['value'], request.form['comment']])
        if not errors:
            manager.writeline('in.txt')
            return redirect('/')
    return render_template('index.html', stock=stock, account=account, errors=errors)

@app.route('/history/')
def history():
    history = manager.history
    # from = manager.history[int(request.form['from'])]
    # to = manager.history[int(request.form['to'])+1]
    return render_template('history.html', history=history)