import json
import urllib
import requests

where = urllib.parse.quote_plus("""
{
    "Year": {
        "$exists": true
    }
}
""")
url = 'https://parseapi.back4app.com/classes/Carmodels_Car_Model_List?limit=10&keys=Make,Year&where=%s' % where
headers = {
    'X-Parse-Application-Id': '1Fq1JQ9T6jfkbcGGOuzGVwMeOaLe6ArsmPKPXvfi', # This is your app's application id
    'X-Parse-REST-API-Key': '9gA1WmxS3RolZChj4tgHkHj3Firlxt6Yn16DsTEi' # This is your app's REST API key
}
data = json.loads(requests.get(url, headers=headers).content.decode('utf-8')) # Here you have the data that you need
for i in data['results']:
    print(i['objectId'])