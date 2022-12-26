import datetime
# from app.api import fetch_from_api
from app.make_celery import make_celery
from app import *
from app.api import fetch_from_api







@celery.task(name='store')
def store():
    fetch_from_api()
    print("Data Stored After 24 Hours")
    # celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "")
    # celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://redis:6379/0")



celery.register_task(store)
