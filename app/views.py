import jwt
import logging


from app import *
from app.schemas import CarSchema
from app.forms import LoginForm, RegistrationForm
from app.consts import sender, recipients
from datetime import datetime, timedelta
from models import Car, User
from flask import render_template, url_for, redirect, jsonify, request, session
from flask_mail import Mail, Message
from functools import wraps


# Decorator for Token Validation
def check_token(func):
    """
    A Decorator to validate user by checking the session token provided by jwt.
    The token must be valid or provided to visit the route (/api).
    It also throws exception on expires token as well.

    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return redirect(url_for('home'))
        try:
            payload = jwt.decode(token, "secret", algorithms=['HS256'])
        except:
            try:
                payload = jwt.decode(
                    token, "refresh_token", algorithms=['HS256'])
            except:
                logging.critical('session expires')
                return redirect(url_for('fetch_from_api'))
        return func(*args, **kwargs)

    return wrapper


# Sending Mail On Login With Unique Link
def email_sending(link):
    """

    link with the token can be mailed to registered user by using this function.
    just modification will be needed to send email to dynamic recipients.

    """
    mail = Mail(app)
    msg = Message(
        'Hello',
        sender=sender,
        recipients=recipients
    )
    msg.body = 'Hello Link For API is ' + '\n' + link
    mail.send(msg)


# API Return Response
@app.route('/api')
@check_token  # Decorator
def fetch_from_api():
    """

    This view function will execute when the decorator mentioned above validates the token.
    After that the function will return all the data stored in database from api.

    """
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)
    cars = db.session.query(Car).paginate(page=page, per_page=per_page)
    meta = {
        'page': cars.page,
        'pages': cars.pages,
        'total_count': cars.total,
        'prev_page': cars.prev_num,
        'next_page': cars.next_num,
        'has_next': cars.has_next,
        'has_prev': cars.has_prev,
    }
    serializer = CarSchema(many=True)
    car_data = serializer.dump(cars)
    return jsonify(
        car_data, meta
    )


# first interface of web application (login_page)
@app.route('/', methods=['GET', 'POST'])
def home():
    """

    This is the first interface of application that requires two fields username and password.
    If username and password is valid by checking from database then it will generate a session_token and refresh_token.
    The user will be routed to api page with token, token will expire after given time and user will be automatically
    shifts to refresh_token if refresh token also expires then user must have to log in again.

    """

    form = LoginForm()
    session_token = ''
    global refresh_token
    if request.method == 'POST':
        user_name = form.username.data
        pass_word = form.password.data
        check_user = db.session.query(User).filter_by(
            username=user_name, password=pass_word).first()
        if check_user:
            # Storing Session
            session['check_user'] = user_name

            # Creating Tokens (Access Token) and (Refresh Token)

            session_token = jwt.encode({"user": user_name,
                                        "exp": datetime.utcnow() + timedelta(seconds=50)},
                                       "secret", algorithm="HS256")
            refresh_token = jwt.encode({"user": user_name,
                                        "exp": datetime.utcnow() + timedelta(seconds=110)},
                                       "refresh_token", algorithm="HS256")
            # Decoding Tokens in UTF-8 Standard
            session_token = session_token.encode().decode('utf-8')
            refresh_token = refresh_token.encode().decode('utf-8')

            try:
                payload = jwt.decode(
                    session_token, "secret", algorithms=['HS256'])
                logging.info(f'{user_name} succesfully logged in and is on Session Token')

                # For email Sending  Just Uncomment And Put Password in email_sending() Function
                # email_sending(link = 'http://127.0.0.1:5000/api?token='+session_token)

                return redirect('api?token=' + session_token)
            except:
                logging.info('User is shifted to Refresh Token')
                return redirect('api?token=' + refresh_token)

        # If Username or Password is Wrong
        else:
            message = 'check username or password'
            return render_template('home.html', form=form, error=message)

    # If Session Is Stored

    else:
        if "check_user" in session:
            try:
                payload = jwt.decode(
                    session_token, "secret", algorithms=['HS256'])
                return redirect('api?token=' + session_token)

            # If Access Token Session Completed Then User Will be automatically Shifted to Refresh TOken and session pops

            except:
                session.pop('check_user', None)
                logging.warning('User is shifted to Refresh Token')

                return redirect('api?token=' + refresh_token)

    return render_template('home.html', form=form)


# register_page of web application

@app.route('/register', methods=['GET', 'POST'])
def register():
    """

    It's a register route to register a new user.
    This route also validates data ex: username must be unique and password must be same.
    
    """

    form = RegistrationForm()
    if request.method == 'POST':
        user_name = form.username.data
        pass_word = form.password.data
        c_password = form.c_password.data
        check_user = db.session.query(User).filter_by(
            username=user_name).first()
        if check_user:
            message = 'Username already taken'
            return render_template('register.html', form=form, error=message)
        elif pass_word != c_password:
            message = 'Password must be same'
            return render_template('register.html', form=form, error=message)
        else:
            user = User(username=user_name, password=pass_word)
            db.session.add(user)
            db.session.commit()
            logging.info('User Succefully Registered')
            return redirect(url_for('home'))
            
    return render_template('register.html', form=form)
