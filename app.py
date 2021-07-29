from flask import Flask, render_template
from accountant import manager

app = Flask(__name__)

@app.route('/')
def homepage():
    stock = manager.stock.items()
    print(stock)
    return render_template('index.html', stock = stock)