from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
import os
from datetime import date

app=Flask(__name__)


basedir = os.path.abspath(os.path.dirname(__file__))

db_file = os.path.join(app.root_path, 'test.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_file}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Customer(db.Model):
    id=db.Column(db.Integer,primary_key=True, autoincrement=True)
    customer_name=db.Column(db.String(100),nullable=False)
    email=db.Column(db.String(200),nullable=False, unique=True)
    address=db.Column(db.String(500),nullable=False)
    total_orders=db.Column(db.Integer,nullable=False)

class Product(db.Model):
    product_id=db.Column(db.Integer,primary_key=True, autoincrement=True)
    product_name=db.Column(db.String(100),nullable=False)
    product_price=db.Column(db.Float,nullable=False)
    product_color=db.Column(db.String(100),nullable=False)
    product_image=db.Column(db.String(100),nullable=False)

class Customer_orders(db.Model):
    order_id=db.Column(db.Integer,primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    product_id=db.Column(db.Integer, db.ForeignKey('product.product_id'))
    price=db.Column(db.Float,nullable=False)
    date_of_purchase=db.Column(db.Date, nullable=False)
    total_paid=db.Column(db.Float,nullable=False)
    order_status=db.Column(db.Boolean, nullable=False, default=False)


app.app_context().push()