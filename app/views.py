from flask import render_template, url_for, redirect, jsonify, request, session
from app.forms import *
from marshmallow import Schema, fields
from app.models import *
from app.task import *
from flask_mail import Mail, Message
import datetime


# Schema For API
class CarSchema(Schema):
    id = fields.String()
    year = fields.Integer()
    make = fields.String()
    created_at = fields.String()
    updated_at = fields.String()



def check_token(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return redirect(url_for('home'))
        try:
            payload = jwt.decode(token, "secret", algorithms=['HS256'])
        except:
            try:
                payload = jwt.decode(token, "refreshtoken", algorithms=['HS256'])
            except:
                return redirect(url_for('khan'))
        return func(*args, **kwargs)

    return wrapper

# Sending Mail On Login With Unique Link
def email_sending(link):
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = 'any@gmail.com'
    app.config['MAIL_PASSWORD'] = 'Any_Password'
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True
    mail = Mail(app)
    # recipient = 'any@protonmail.com'
    # subject = 'From PortFolio'
    # message = 'Email : ' + 'any@gmail.com' + '\n' + 'Phone :' + 'XXXXXXXXX'+ '\n' + 'Name : ' + \
    #           'Ali Fayyaz Durrani'+ '\n' + 'Message:' + 'this is test message'
    msg = Message(
        'Hello',
        sender='any@gmail.com',
        recipients=['any@protonmail.com'])
    msg.body = 'Hello Link For API is ' + '\n' + link
    mail.send(msg)


# redis port number on which local server running



@app.route('/api')
@check_token  # Decoratar
def khan():
    # To Fetch Data That is stored in Database From API

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
    global session_token
    global refresh_token
    if request.method == 'POST':
        user_name = form.username.data
        pass_word = form.password.data
        check_user = User.query.filter_by(username=user_name, password=pass_word).first()
        if check_user != None:
            # Storing Session
            session['check_user'] = user_name

            # Creating Tokens (Access Token) and (Refresh Token)

            token = jwt.encode({"user": user_name,
                                "exp": datetime.datetime.utcnow() + timedelta(seconds=15)},
                               "secret", algorithm="HS256")
            refresh_token = jwt.encode({"user": user_name,
                                        "exp": datetime.datetime.utcnow() + timedelta(seconds=30)},
                                       "refreshtoken", algorithm="HS256")

            # Decoding Tokens in UTF-8 Standard
            session_token = token.encode().decode('utf-8')
            refresh_token = refresh_token.encode().decode('utf-8')

            try:
                payload = jwt.decode(session_token, "secret", algorithms=['HS256'])

                # For email Sending  Just Uncomment And Put Password in email_sending() Function
                # email_sending(link = 'http://127.0.0.1:5000/api?token='+session_token)

                return redirect('api?token=' + session_token)
            except:

                return redirect('api?token=' + refresh_token)

        # If Username or Password is Wrong

        else:
            message = 'check username or password'
            return render_template('home.html', form=form, error=message)



    # If Session Is Stored

    else:
        if "check_user" in session:
            try:
                payload = jwt.decode(session_token, "secret", algorithms=['HS256'])
                return redirect('api?token=' + session_token)

            # If Access Token Session Completed Then User Will be automatically Shifted to Refresh TOken and session pops

            except:
                session.pop('check_user', None)
                return redirect('api?token=' + refresh_token)

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
