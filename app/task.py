from app import celery
from app.api import fetch_from_api


@celery.task(name='store')
def store():
    fetch_from_api()
    print("Data Stored After 24 Hours")


celery.register_task(store)
