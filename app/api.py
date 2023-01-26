import json
import logging
import requests
import urllib

from app import db
from app.models import Car


# Function for Celery task to fetch data
def fetch_from_api():
    where = urllib.parse.quote_plus("""
    {
        "Year": {
            "$gte": 2012
        }
    }
    """)
    url = f'https://parseapi.back4app.com/classes/Carmodels_Car_Model_List?limit=10&keys=Make,Year&where={where}'
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
        if err.status_code == '401':
            logging.critical('Unauthorized response from API..')
        elif err.status_code == '404':
            logging.critical('No Found response from API..')
        elif err.status_code == '407':
            logging.critical('Authentication required from API..')
        elif err.status_code == '500':
            logging.critical('Internal Server Error from API..')
        elif err.status_code == '502':
            logging.critical('Bad Gateway response from API..')
        elif err.status_code == '505':
            logging.critical('HTTP version not supported response from API..')
        elif err.status_code == '503':
            logging.critical('Service not available response from API..')
        else:
            logging.critical(err.status_code + 'Response from API..')
        
        return
    database_data = db.session.query(Car).all()
    list_sync = []
    for j in data['results']:
        try:
            list_sync.index(j['objectId'])
        except:
            list_sync.append(j['objectId'])

    for i in database_data:
        try:
            list_sync.index(i.id)
        except:
            deleting = db.session.query(Car).filter_by(id = id.i).delete()
            db.session.commit()
    for i in data['results']:
        check = db.session.query(Car).filter_by(id=i['objectId']).first()
        if not check:
            car = Car(id=i['objectId'], year=i['Year'], make=i['Make'], created_at=i['createdAt'],
                      updated_at='saldkjaskldj')
            db.session.add(car)
            db.session.commit()
        else:
            if check.updated_at == i['updatedAt']:
                pass
            else:
                check.id = i['objectId']
                check.year = i['Year']
                check.make = i['Make']
                check.created_at = i['createdAt']
                check.updated_at = i['updatedAt']
                db.session.commit()           
                print("Data Updated at completed")
    return 'Data Synced'
    