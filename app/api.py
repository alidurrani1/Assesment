import json
import requests
import urllib
import logging

from app import db
from models import Car


# Function for Celery task to fetch data
def fetch_from_api():
    where = urllib.parse.quote_plus("""
    {
        "Year": {
            "$gte": 2012
        }
    }
    """)
    url = 'https://parseapi.back4app.com/classes/Carmodels_Car_Model_List?limit=10&keys=Make,Year&where=%s' % where
    headers = {
        # This is your app's application id
        'X-Parse-Application-Id': '1Fq1JQ9T6jfkbcGGOuzGVwMeOaLe6ArsmPKPXvfi',
        # This is your app's REST API key
        'X-Parse-REST-API-Key': '9gA1WmxS3RolZChj4tgHkHj3Firlxt6Yn16DsTEi'
    }

    try:
        data = json.loads(
            requests.get(url, headers=headers).content.decode('utf-8'))  # Here you have the data that you need
    except requests.exceptions.HTTPError as err:
        logging.critical('Bad Request Code')
        return
        # raise err

    for i in data['results']:
        check = db.session.query(Car).filter_by(id=i['objectId']).first()
        if not check:
            car = Car(id=i['objectId'], year=i['Year'], make=i['Make'], created_at=i['createdAt'],
                      updated_at=i['updatedAt'])
            db.session.add(car)
            db.session.commit()
        
