from flask import Flask, render_template,url_for,redirect,jsonify,request
from flask_sqlalchemy import SQLAlchemy
from forms import *
import json
import urllib
import requests
from flask_celery import make_celery
from marshmallow import Schema,fields
import time 
from datetime import datetime









#Creating App and database configurations
app = Flask(__name__)
app.app_context().push()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'Any_Key'
db = SQLAlchemy(app)
db.create_all()

# Creating Database    
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    username = db.Column(db.String(28),nullable=False, unique = True)
    password = db.Column(db.String(28),nullable=False)    

# Creating Database for api   

class Car(db.Model):
    id = db.Column(db.String(30), primary_key=True)
    year = db.Column(db.Integer,nullable=False)
    make = db.Column(db.String(28),nullable=False)
    created_at = db.Column(db.String(60),nullable=False)
    updated_at = db.Column(db.String(60),nullable=False)

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def get_by_id(cls,id):
        return cls.query.get_or_404(id)


#creating schema of api by extending it with marshmallow_Schema
class CarSchema(Schema):
    id = fields.String()
    year = fields.Integer()
    make = fields.String()
    created_at = fields.String()
    updated_at = fields.String()


#redis port number on which local server running
app.config.update(CELERY_CONFIG={
    'broker_url': 'redis://localhost:6379',
    'result_backend': 'redis://localhost:6379',
})
celery = make_celery(app)

@celery.task(name = 'data_api.store')
def store(time):
    now = datetime.now()
    current_time = now.strftime('%H:%M%S')
    if current_time == '12:00:00':
        data = json.loads(requests.get(url, headers=headers).content.decode('utf-8')) # Here you have the data that you need
        for i in data['results']:
            check = Car.query.filter_by(id=i['objectId']).first()
            if check == None:
                car = Car(id = i['objectId'],year = i['Year'],make = i['Make'],created_at = i['createdAt'], updated_at = i['updatedAt'])
                db.session.add(car)
                db.session.commit()      
            else:
                pass
        return 'Stored Completly new data'
    else:
        return 'Not a Time for store'
    



#Api Configurations

where = urllib.parse.quote_plus("""
{
    "Year": {
        "$gte": 2012
    }
}
""")
url = 'https://parseapi.back4app.com/classes/Carmodels_Car_Model_List?limit=10&keys=Make,Year&where=%s' % where
headers = {
    'X-Parse-Application-Id': '1Fq1JQ9T6jfkbcGGOuzGVwMeOaLe6ArsmPKPXvfi', # This is your app's application id
    'X-Parse-REST-API-Key': '9gA1WmxS3RolZChj4tgHkHj3Firlxt6Yn16DsTEi' # This is your app's REST API key
}




#fetching data from api and storing in Database
#created api to display fetched data (with serailizer using marshmallow schema)
@app.route('/home')
def index():
    now = datetime.now()
    current_time = now.strftime('%H:%M%S')
    store.delay(current_time)
    # data = json.loads(requests.get(url, headers=headers).content.decode('utf-8')) # Here you have the data that you need

    # for i in data['results']:
    #      check = Car.query.filter_by(id=i['objectId']).first()
    #      if check == None:
    #         car = Car(id = i['objectId'],year = i['Year'],make = i['Make'],created_at = i['createdAt'], updated_at = i['updatedAt'])
    #         db.session.add(car)
    #         db.session.commit()      
    #      else:
    #         pass
    # result = add_together.delay(23, 42)
    page = request.args.get('page',1,type=int)
    per_page = request.args.get('per_page',5,type=int)
    cars = Car.query.all()
    serializer = CarSchema(many = True)
    car_data = serializer.dump(cars)
    return jsonify(
        car_data
    )


#first interface of web application (login_page)
@app.route('/' , methods=['GET','POST'])
def home():
    form = LoginForm()
    if request.method == 'POST':
        user_name = form.username.data
        pass_word = form.password.data
        check_user = User.query.filter_by(username = user_name,password=pass_word).first()
        if check_user != None:
            return redirect(url_for('index'))
        else:
            message = 'check username or password'
            return render_template('home.html',form = form,error = message)
    return render_template('home.html',form = form)
    

#register_page of web application
@app.route('/register' , methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if request.method == 'POST':
                user_name = form.username.data
                pass_word = form.password.data
                c_password = form.c_password.data
                check_user = User.query.filter_by(username = user_name).first()
                print(check_user)
                if check_user != None:
                    message = 'Username already taken'
                    return render_template('register.html',form = form, error = message)
                elif pass_word != c_password:
                    message = 'Password must be same'
                    return render_template('register.html',form = form, error = message)
                else:
                    user = User(username = user_name,password = pass_word)
                    print(user)
                    db.session.add(user)
                    db.session.commit()
                    return redirect(url_for('home'))
    return render_template('register.html',form = form)
    
    
    
if __name__ == "__main__":
    app.run(host='127.0.0.1',port=8080,debug=True)