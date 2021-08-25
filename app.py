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


errors = {}

@app.route('/', methods = ["GET", "POST"])
def homepage():
    stock = db.session.query(Stock).all()
    account = db.session.query(Account).filter(Account.id == 1).first()
    account = account.account
    return render_template('index.html', stock=stock, account=account)

@app.route('/balance/', methods = ["GET", "POST"])
def balance():
    account = db.session.query(Account).filter(Account.id == 1).first()
    if request.method == "POST":
        action = request.form.get('action')
        if action not in ['buy', 'sell', 'balance']:
            errors['action'] = 'Choose an action!'
        if account.account + int(request.form['value']) < 0:
            errors['money'] = 'Not enough money!'
        if action == 'balance':
            app4 = History(
                what_action=1,
                first_action=request.form['value'],
                second_action=request.form['comment'],
                third_action=0
            )
            new_account = account.account + int(request.form['value'])
            account.account = new_account
            db.session.add(app4)
            db.session.add(account)
        if not errors:
            db.session.commit()
            return redirect('/balance/')
    return render_template('balance.html', errors=errors)

@app.route('/buysell/', methods=["GET", "POST"])
def buysell():
    account = db.session.query(Account).filter(Account.id == 1).first()
    if request.method == "POST":
        action = request.form.get('action')
        if action not in ['buy', 'sell', 'balance']:
            errors['action'] = 'Choose an action!'
        if action == 'buy':
            if account.account - (int(request.form['unit_price']) * int(request.form['qty'])) < 0:
                errors['money'] = 'Not enough money!'
            stock = db.session.query(Stock).all()
            dict_stock = []
            for item in stock:
                dict_stock.append(item.product)
            if request.form['product'] not in dict_stock:
                app1 = Stock(
                    product=request.form['product'],
                    qty=request.form['qty']
                )
                db.session.add(app1)
                db.session.commit()
            stock = db.session.query(Stock).filter(Stock.product == request.form['product']).first()
            app2 = History(
                what_action=3,
                first_action=stock.id,
                second_action=int(request.form['unit_price']),
                third_action=request.form['qty']
            )
            new_account = account.account - (int(request.form['unit_price']) * int(request.form['qty']))
            account.account = new_account
            db.session.add(app2)
            db.session.add(account)
            if request.form['product'] in dict_stock:
                new_stock = int(stock.qty) + int(request.form['qty'])
                stock.qty = new_stock
                db.session.add(stock)
        if action == 'sell':
            stock = db.session.query(Stock).filter(Stock.product == request.form['product']).first()
            if int(stock.qty) - int(request.form['qty']) < 0:
                errors['stock'] = 'Not enough product in stock!'
            app2 = History(
                what_action=2,
                first_action=stock.id,
                second_action=int(request.form['unit_price']),
                third_action=request.form['qty']
            )
            new_account = account.account + (int(request.form['unit_price']) * int(request.form['qty']))
            account.account = new_account
            stock.qty -= int(request.form['qty'])
            db.session.add(app2)
            db.session.add(account)
            db.session.add(stock)
        if not errors:
            db.session.commit()
            return redirect('/buysell/')
    return render_template('buysell.html', errors=errors)

@app.route('/history/', methods=["GET", "POST"])
def history(from_history=None, to_history=None):
    history = db.session.query(History).all()
    if request.method == "POST":
        if not request.form['to']:
            from_history = int(request.form['from'])
            to_history = history[-1]
            history = history[(from_history - 1):]
        elif request.form['from'] and request.form['to']:
            from_history = int(request.form['from'])
            to_history = int(request.form['to'])
            history = history[(from_history - 1):to_history]
    return render_template('history.html', history=history)
