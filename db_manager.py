from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///accountant.db'
app.config["SECRET_KEY"] = "Tajny klucz"

db = SQLAlchemy(app)


class Inventory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product = db.Column(db.String)
    price = db.Column(db.Integer)
    quantity = db.Column(db.Integer)

# Inicjalizacja bazy danych
with app.app_context():
    db.create_all()
    db.session.commit()
