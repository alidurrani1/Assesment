import jwt

from app.make_celery import *
from celery.schedules import crontab
from datetime import datetime,timedelta
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.app_context().push()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'Any_Key'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'any@gmail.com'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

# app.config.update(CELERY_CONFIG={
#     'broker_url': 'redis://localhost:6379/0',
#     'result_backend': 'redis://localhost:6379/0',
# })
app.config.update(CELERY_CONFIG={
    'broker_url': 'redis://redis:6379/0',
    'result_backend': 'redis://redis:6379/0',
})
app.config.update(CELERYBEAT_SCHEDULE={
    'say-every-5-seconds': {
        'task': 'store',
        "schedule": crontab(hour='*/24'),
    }
})

celery = make_celery(app)
# celery = make_celery(app)
db = SQLAlchemy(app)
db.init_app(app)
db.create_all()
csrf = CSRFProtect()
csrf.init_app(app)

from app import views
