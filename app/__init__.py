from app.make_celery import make_celery
from config import Config, EmailConfigurations, CeleryConfigurations
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.config.from_object(Config)
app.config.from_object(EmailConfigurations)
db = SQLAlchemy(app)
from models import car_model, user_model

# app.config.update(CELERY_CONFIG={
#     'broker_url': 'redis://localhost:6379/0',
#     'result_backend': 'redis://localhost:6379/0',
# })


with app.app_context():
    db.create_all()

app.config.from_object(CeleryConfigurations)
celery = make_celery(app)

csrf = CSRFProtect()
csrf.init_app(app)

from app import views
