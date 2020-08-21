from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'c34143464249e4b2c000f1a05e5172c7'

from app import views
