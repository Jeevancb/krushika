import numpy as np
from sklearn.linear_model import LinearRegression
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__)

#SQLITE Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

#CSRF Token
app.config['SECRET_KEY'] = "secretkey123"

db = SQLAlchemy(app)

class Exp_tb(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer, unique=True, nullable=False)
    seed_cost = db.Column(db.Integer,nullable=False)
    fertilizer_cost = db.Column(db.Integer,nullable=False)
    irrigation_cost = db.Column(db.Integer,nullable=False)
    labour_cost = db.Column(db.Integer,nullable=False)
    transportation_cost = db.Column(db.Integer,nullable=False)
    other_cost = db.Column(db.Integer,nullable=False)
    yield_amount = db.Column(db.Integer,nullable=False)
    crop_price = db.Column(db.Integer,nullable=False)
    total_cost = db.Column(db.Integer,nullable=False)
    revenue = db.Column(db.Integer,nullable=False)
    profit = db.Column(db.Integer,nullable=False)

def pricePredict5(inp):

    retrieved_data = Exp_tb.query.all()
    exp_data_year = []
    req_data = []

    
    for i in retrieved_data:
        exp_data_year.append(i.year)

    if inp=='seed_cost':
        for i in retrieved_data:
            req_data.append(i.seed_cost)

    if inp=='fertilizer_cost':
        for i in retrieved_data:
            req_data.append(i.fertilizer_cost)

    if inp=='irrigation_cost':
        for i in retrieved_data:
            req_data.append(i.irrigation_cost)

    if inp=='labour_cost':
        for i in retrieved_data:
            req_data.append(i.labour_cost)

    if inp=='transportation_cost':
        for i in retrieved_data:
            req_data.append(i.transportation_cost)

    if inp=='other_cost':
        for i in retrieved_data:
            req_data.append(i.other_cost)

    if inp=='yield_amount':
        for i in retrieved_data:
            req_data.append(i.yield_amount)

    if inp=='crop_price':
        for i in retrieved_data:
            req_data.append(i.crop_price)

    if inp=='total_cost':
        for i in retrieved_data:
            req_data.append(i.total_cost)

    if inp=='revenue':
        for i in retrieved_data:
            req_data.append(i.revenue)

    if inp=='profit':
        for i in retrieved_data:
            req_data.append(i.profit)
    


    y = np.array(req_data).reshape(-1, 1)
    X = np.array(exp_data_year).reshape(-1, 1)

    model = LinearRegression()
    model.fit(X,y)

    X_predict = [(exp_data_year[-1]+1),(exp_data_year[-1]+2),(exp_data_year[-1]+3),(exp_data_year[-1]+4),(exp_data_year[-1]+5)]
    X_predict = np.array(X_predict).reshape(-1, 1)

    y_predict = model.predict(X_predict)

    y_out = y_predict.flatten()

    return y_out


print(pricePredict5("seed_cost"))