from flask import Flask, render_template, request, redirect
from accountant import manager, reader
from flask_sqlalchemy import SQLAlchemy
from flask_alembic import Alembic


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

db = SQLAlchemy(app)


class History(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    what_action = db.Column(db.Integer, unique=False)
    first_action = db.Column(db.Integer, unique=False)
    second_action = db.Column(db.String(120), unique=False)
    third_action = db.Column(db.Integer, unique=False)


class Actions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    what_action = db.Column(db.String(32), unique=True)


class Stock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product = db.Column(db.String(64), unique=True)
    qty = db.Column(db.Integer, unique=False)


class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account = db.Column(db.Integer, unique=False)


db.create_all()
alembic = Alembic(app)
alembic.init_app(app)

# db.session.query(Account).filter(Account.id==1).delete()
# db.session.commit()
# app_1 = Account(account=1000000)
# # app_2 = History(what_action=1, first_action=1000000, second_action='wplata poczatkowa', third_action=0)
# db.session.add(app_1)
# # db.session.add(app_2)
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
    account = db.session.query(Account).filter(Account.id == 1).first()
    account = account.account
    errors = {}
    if request.method == "POST":
        action = request.form.get('action')
        if action not in ['buy', 'sell', 'balance']:
            errors['action'] = 'Choose an action!'
        last_account = db.session.query(Account).filter(Account.id == 1).first()
        if last_account.account + int(request.form['value']) < 0 or \
                last_account.account + int(request.form['unit_price']) < 0:
            errors['money'] = 'Not enough money!'
        stock = db.session.query(Stock).filter(Stock.product == request.form['product']).all()
        if action == 'buy':
            if str(request.form['product']) == str(stock.product):
                new_stock = int(stock.qty) + int(request.form['qty'])
            app1 = Stock(
                product=request.form['product'],
                qty=request.form['qty']
            )
            first_action = db.session.query(Stock).filter(Stock.product == request.form['product']).first()
            app2 = History(
                what_action=3,
                first_action=first_action.id,
                second_action=int(request.form['unit_price']),
                third_action=request.form['qty']
            )
            new_account = last_account.account - (int(request.form['unit_price']) * int(request.form['qty']))
            last_account.account = new_account
            db.session.add(app1)
            db.session.add(app2)
            db.session.add(new_stock)
            db.session.add(last_account)
        if action == 'sell':
            if stock.qty - int(request.form['qty']) < 0:
                errors['stock'] = 'Not enough product in stock!'
            app1 = Stock(
                product=request.form['product'],
                qty=request.form['qty']
            )
            app2 = History(
                what_action=2,
                first_action=db.session.query(Stock).filter(Stock.product == request.form['product']).first(),
                second_action=int(request.form['unit_price']),
                third_action=request.form['qty']
            )
            new_account = last_account.account + (int(request.form['unit_price']) * int(request.form['qty']))
            last_account.account = new_account
            db.session.add(app1)
            db.session.add(app2)
            db.session.add(last_account)
        if action == 'balance':
            app4 = History(
                what_action=1,
                first_action=request.form['value'],
                second_action=request.form['comment'],
                third_action=0
            )
            last_account = db.session.query(Account).filter(Account.id == 1).first()
            new_account = last_account.account + int(request.form['value'])
            last_account.account = new_account
            db.session.add(app4)
            db.session.add(last_account)
        if not errors:
            db.session.commit()
            return redirect('/')
    return render_template('index.html', stock=stock, account=account, errors=errors)

@app.route('/history/')
def history():
    history = db.session.query(History).all()
    # from_history = db.session.query(History).filter(History.id == int(request.form['from'])).first()
    # to_history = db.session.query(History).filter(History.id == int(request.form['to'])+1).first()
    return render_template('history.html', history=history)
