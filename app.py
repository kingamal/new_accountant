from flask import Flask, render_template
from accountant import manager

app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def homepage():
    stock = manager.stock.items()
    return render_template('index.html', stock = stock)