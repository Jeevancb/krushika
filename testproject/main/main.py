from flask_bcrypt import Bcrypt
from enum import unique
import io
import base64
import time
import numpy as np
from sklearn.linear_model import LinearRegression

# Flask Library
from flask import Flask, render_template, url_for, redirect, request, send_file

# Flask SQL Connectivity
from flask_sqlalchemy import SQLAlchemy

# forms
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, DecimalField, SelectField, IntegerField
from wtforms.validators import InputRequired, DataRequired, Length, NumberRange, ValidationError

# Date Module
from datetime import datetime

# Flask Login Module
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user

# importing classes from forms.py
from forms import SoilTestForm, ExpenditureForm

# Matplotlib for visualization
import matplotlib.pyplot as plt

# Flask app creation
app = Flask(__name__)

# SQLITE Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

# CSRF Token
app.config['SECRET_KEY'] = "secretkey123"

# Database Object
db = SQLAlchemy(app)

# Password Hashing
bcrypt = Bcrypt(app)
# Databases

# Registration Form


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)


class Exp_tb(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer, unique=True, nullable=False)
    seed_cost = db.Column(db.Integer, nullable=False)
    fertilizer_cost = db.Column(db.Integer, nullable=False)
    irrigation_cost = db.Column(db.Integer, nullable=False)
    labour_cost = db.Column(db.Integer, nullable=False)
    transportation_cost = db.Column(db.Integer, nullable=False)
    other_cost = db.Column(db.Integer, nullable=False)
    yield_amount = db.Column(db.Integer, nullable=False)
    crop_price = db.Column(db.Integer, nullable=False)
    total_cost = db.Column(db.Integer, nullable=False)
    revenue = db.Column(db.Integer, nullable=False)
    profit = db.Column(db.Integer, nullable=False)


class St_results(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ph = db.Column(db.Integer, nullable=False)
    magnesium = db.Column(db.Integer, nullable=False)
    phosphorus = db.Column(db.Integer, nullable=False)
    potassium = db.Column(db.Integer, nullable=False)
    calcium = db.Column(db.Integer, nullable=False)
    boron = db.Column(db.Integer, nullable=False)
    iron = db.Column(db.Integer, nullable=False)
    zinc = db.Column(db.Integer, nullable=False)
    manganese = db.Column(db.Integer, nullable=False)
    soiltype = db.Column(db.String(50), nullable=False)


class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[InputRequired(), Length(
        min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Register')

    # Unique Username Validation
    def validate_username(self, username):
        existing_user_username = User.query.filter_by(
            username=username.data).first()
        if existing_user_username:
            raise ValidationError(
                'That username already exists.')

# Login Form


class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[InputRequired(), Length(
        min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Login')


# Login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# ROUTES

# Home page
@app.route('/')
def home_page1():
    return render_template('index.html')

# Soil Test Page


@app.route('/soiltest', methods=['GET', 'POST'])
def soil_test_page():
    global nutrient_values
    ph_value = None
    form = SoilTestForm()

    # On submit button click below statements executes
    if form.validate_on_submit():
        ph_value = form.ph_value.data
        form.ph_value = ''

        magnesium_value = form.magnesium_value.data
        form.magnesium_value = ''

        phosphorus_value = form.phosphorus_value.data
        form.phosphorus_value = ''

        potassium_value = form.potassium_value.data
        form.potassium_value = ''

        calcium_value = form.calcium_value.data
        form.calcium_value = ''

        boron_value = form.boron_value.data
        form.boron_value = ''

        iron_value = form.iron_value.data
        form.iron_value = ''

        zinc_value = form.zinc_value.data
        form.zinc_value = ''

        manganese_value = form.manganese_value.data
        form.manganese_value = ''

        soiltype_value = form.soil_type.data

        nutrient_values = [
            ph_value,
            magnesium_value,
            phosphorus_value,
            potassium_value,
            calcium_value,
            boron_value,
            iron_value,
            zinc_value,
            manganese_value,
            soiltype_value
        ]
        new_test = St_results(ph=ph_value, magnesium=magnesium_value,
                              phosphorus=phosphorus_value, potassium=potassium_value, calcium=calcium_value,
                              boron=boron_value, iron=iron_value, zinc=zinc_value, manganese=manganese_value, soiltype=soiltype_value)
        db.session.add(new_test)
        db.session.commit()
        return redirect('result')

    return render_template('soiltest.html', ph_value=ph_value, form=form)

# Results Page


@app.route('/result', methods=['GET', 'POST'])
def soiltest_results():
    global nutrient_values
    n_labels = [
        'Magnesium',
        'Phosphorus',
        'Potassium',
        'Calcium',
        'Boron',
        'Iron',
        'Zinc',
        'Manganese'
    ]

    recent_st = db.session.query(St_results).order_by(
        St_results.id.desc()).first()
    ph_value = recent_st.ph
    n_values = [recent_st.magnesium, recent_st.phosphorus, recent_st.potassium,
                recent_st.calcium, recent_st.boron, recent_st.iron,
                recent_st.zinc, recent_st.manganese]
    return render_template('soiltest_result.html', n_labels=n_labels, n_values=n_values, ph_value=ph_value)

# Expenditures Page


@app.route('/expenditure', methods=['GET', 'POST'])
def expenditure_page():
    global cost_values, exp_data_total, exp_data_year
    seed_cost_value = None
    form = ExpenditureForm()

    # On submit button click below statements executes
    if form.validate_on_submit():

        # REFERENCE
        #new_user = User(username=form.username.data, password=hashed_password)
        # db.session.add(new_user)
        # db.session.commit()
        if request.method == "POST":

            new_expenditure = Exp_tb(
                year=form.year_field.data,
                seed_cost=form.seed_cost.data,
                fertilizer_cost=form.fertilizer_cost.data,
                irrigation_cost=form.irrigation_cost.data,
                labour_cost=form.labour_cost.data,
                transportation_cost=form.transportation_cost.data,
                other_cost=form.other_cost.data,
                yield_amount=form.yield_amount.data,
                crop_price=form.crop_price.data,
                total_cost=(form.seed_cost.data
                            + form.fertilizer_cost.data
                            + form.irrigation_cost.data
                            + form.labour_cost.data
                            + form.transportation_cost.data
                            + form.other_cost.data),
                revenue=(form.yield_amount.data*form.crop_price.data),
                profit=((form.yield_amount.data*form.crop_price.data)-(form.seed_cost.data
                                                                       + form.fertilizer_cost.data
                                                                       + form.irrigation_cost.data
                                                                       + form.labour_cost.data
                                                                       + form.transportation_cost.data
                                                                       + form.other_cost.data))
            )

            form.year_field = ''
            form.seed_cost = ''
            form.fertilizer_cost = ''
            form.irrigation_cost = ''
            form.labour_cost = ''
            form.transportation_cost = ''
            form.other_cost = ''
            form.yield_amount = ''
            form.crop_price = ''

            db.session.add(new_expenditure)
            db.session.commit()
            exp_data_year = []
            exp_data_total = []
            return redirect('expenditure')

    return render_template('expenditure.html', seed_cost_value=seed_cost_value, form=form)

# login page


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect('/')

    return render_template('login.html', form=form)


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout_page():
    logout_user()
    return redirect('/')


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect('/login')

    return render_template('register.html', form=form)

# Phases Page


@app.route('/phases')
def phases_page():
    return render_template('phases.html'  # , len=len(progress_bar), progress_bar=progress_bar)
                           )


# About Page
@app.route('/about')
def about_page():
    return render_template('about.html')


@app.route('/expenditure/dashboard')
@login_required
def exp_dashboard():
    retrieved_data = Exp_tb.query.all()
    exp_data_year = []
    exp_data_seed = []
    exp_data_fert = []
    exp_data_irr = []
    exp_data_lab = []
    exp_data_transp = []
    exp_data_other = []
    exp_data_yield = []
    exp_data_cprice = []
    exp_data_tcost = []
    exp_data_revenue = []
    exp_data_profit = []

    for i in retrieved_data:
        exp_data_year.append(str(i.year))
        exp_data_seed.append(i.seed_cost)
        exp_data_fert.append(i.fertilizer_cost)
        exp_data_irr.append(i.irrigation_cost)
        exp_data_lab.append(i.labour_cost)
        exp_data_transp.append(i.transportation_cost)
        exp_data_other.append(i.other_cost)
        exp_data_yield.append(i.yield_amount)
        exp_data_cprice.append(i.crop_price)
        exp_data_tcost.append(i.total_cost)
        exp_data_revenue.append(i.revenue)
        exp_data_profit.append(i.profit)

    def avglist(lst):
        return round((sum(lst)/len(lst)), 1)

    r_labels = exp_data_year
    r_values = exp_data_revenue

    cp_values = exp_data_tcost

    ae_labels = ['Seeds', 'Fertilizer', 'Irrigation',
                 'Labour', 'Transportation', 'Other']
    ae_values = [avglist(exp_data_seed), avglist(exp_data_fert),
                 avglist(exp_data_irr), avglist(
                     exp_data_lab), avglist(exp_data_transp),
                 avglist(exp_data_other)]

    def pricePredict5(inp):

        retrieved_data = Exp_tb.query.all()
        exp_data_year = []
        req_data = []

        for i in retrieved_data:
            exp_data_year.append(i.year)

        if inp == 'seed_cost':
            for i in retrieved_data:
                req_data.append(i.seed_cost)

        if inp == 'fertilizer_cost':
            for i in retrieved_data:
                req_data.append(i.fertilizer_cost)

        if inp == 'irrigation_cost':
            for i in retrieved_data:
                req_data.append(i.irrigation_cost)

        if inp == 'labour_cost':
            for i in retrieved_data:
                req_data.append(i.labour_cost)

        if inp == 'transportation_cost':
            for i in retrieved_data:
                req_data.append(i.transportation_cost)

        if inp == 'other_cost':
            for i in retrieved_data:
                req_data.append(i.other_cost)

        if inp == 'yield_amount':
            for i in retrieved_data:
                req_data.append(i.yield_amount)

        if inp == 'crop_price':
            for i in retrieved_data:
                req_data.append(i.crop_price)

        if inp == 'total_cost':
            for i in retrieved_data:
                req_data.append(i.total_cost)

        if inp == 'revenue':
            for i in retrieved_data:
                req_data.append(i.revenue)

        if inp == 'profit':
            for i in retrieved_data:
                req_data.append(i.profit)

        y = np.array(req_data).reshape(-1, 1)
        X = np.array(exp_data_year).reshape(-1, 1)

        model = LinearRegression()
        model.fit(X, y)

        X_predict = [(exp_data_year[-1]+1), (exp_data_year[-1]+2),
                     (exp_data_year[-1]+3), (exp_data_year[-1]+4), (exp_data_year[-1]+5)]
        X_predict = np.array(X_predict).reshape(-1, 1)

        y_predict = model.predict(X_predict)

        y_out = y_predict.flatten()

        return y_out

    exp_year_uninc = []
    for i in retrieved_data:
        exp_year_uninc.append(i.year)

    pdct_profit_labels = [(exp_year_uninc[-1]+1), (exp_year_uninc[-1]+2),
                          (exp_year_uninc[-1]+3), (exp_year_uninc[-1]+4), (exp_year_uninc[-1]+5)]
    pdct_profit_values = pricePredict5('revenue')
    pdct_profit_values_r = []
    for i in pdct_profit_values:
        pdct_profit_values_r.append(round(i))

    return render_template('exp_dashboard.html', r_labels=r_labels, r_values=r_values, cp_values=cp_values, ae_labels=ae_labels, ae_values=ae_values, pdct_profit_values=pdct_profit_values_r, pdct_profit_labels=pdct_profit_labels)


@app.route('/expenditure/delete_records')
@login_required
def delete_records():
    return render_template('delete_confirmation.html')


@app.route('/expenditure/exp_table_delete')
@login_required
def exp_table_delete():
    Exp_tb.query.delete()
    db.session.commit()
    return redirect('/expenditure')


# Run Main Function
if __name__ == "__main__":
    app.run(host="0.0.0.0", use_reloader=True, debug=True)
