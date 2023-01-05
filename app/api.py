import json
import requests
import urllib

from app.models import *



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
        'X-Parse-Application-Id': '1Fq1JQ9T6jfkbcGGOuzGVwMeOaLe6ArsmPKPXvfi',  # This is your app's application id
        'X-Parse-REST-API-Key': '9gA1WmxS3RolZChj4tgHkHj3Firlxt6Yn16DsTEi'  # This is your app's REST API key
    }
    data = json.loads(
        requests.get(url, headers=headers).content.decode('utf-8'))  # Here you have the data that you need

    for i in data['results']:
        check = Car.query.filter_by(id=i['objectId']).first()
        if check == None:
            car = Car(id=i['objectId'], year=i['Year'], make=i['Make'], created_at=i['createdAt'],
                      updated_at=i['updatedAt'])
            db.session.add(car)
            db.session.commit()
        else:
            pass
