import json

import jwt
from flask import render_template, url_for, redirect, jsonify, request, session
from app.forms import *
from marshmallow import Schema, fields
from app.models import *
from app import app
from app.task import *
import datetime


class CarSchema(Schema):
    id = fields.String()
    year = fields.Integer()
    make = fields.String()
    created_at = fields.String()
    updated_at = fields.String()


# redis port number on which local server running

# def check_token(func):
#     @wraps(func)
#     def wrapper(*args, **kwargs):
#         token = request.args.get('token')
#         if not token:
#             return redirect('login')
#
#         return func(*args, **kwargs)
#
#     return wrapper


@app.route('/api')
# @check_token
def khan():
    # store.delay()
    # if not session.get('logged-in'):
    #     return redirect('home')
    # else:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 5, type=int)

        cars = Car.query.all()
        serializer = CarSchema(many=True)
        car_data = serializer.dump(cars)
        return jsonify(
            car_data
        )


# first interface of web application (login_page)
@app.route('/', methods=['GET', 'POST'])
def home():
    form = LoginForm()
    if request.method == 'POST':
        user_name = form.username.data
        pass_word = form.password.data
        check_user = User.query.filter_by(username=user_name, password=pass_word).first()
        if check_user != None:
            #Currently Working on JWT

            # session['logged_in'] = True
            # token = jwt.encode({
            #     'user': user_name,
            #     'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=60)
            # }, app.config['SECRET_KEY'])
            #
            # return jsonify({'token': token.encode().decode('utf-8')})
            return redirect('khan')
        else:
            message = 'check username or password'
            return render_template('home.html', form=form, error=message)
    return render_template('home.html', form=form)


# register_page of web application


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if request.method == 'POST':
        user_name = form.username.data
        print(user_name)
        pass_word = form.password.data
        c_password = form.c_password.data
        check_user = User.query.filter_by(username=user_name).first()
        print(check_user)
        if check_user != None:
            message = 'Username already taken'
            return render_template('register.html', form=form, error=message)
        elif pass_word != c_password:
            message = 'Password must be same'
            return render_template('register.html', form=form, error=message)
        else:
            user = User(username=user_name, password=pass_word)
            print(user)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('home'))
    return render_template('register.html', form=form)
