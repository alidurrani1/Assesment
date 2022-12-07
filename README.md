open python terminal and run this commands
from app import db,User,Car
db.create_all()
User.query.all()
Car.query.all()




python .\app.py for windows
python ./app.py or app.py

must install redis for backend functionallity of storing dat
I've used linux to complete this project 
the command I've used

sudo apt-get install redis            

celery -A app.celery worker --loglevel=DEBUG (for celery)
