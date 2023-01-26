from app import celery
from app.api import fetch_from_api


@celery.task(name='store')
def store():
    fetch_from_api()
    return "Data Synced"

celery.register_task(store)
