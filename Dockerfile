FROM python:3.9
# Create app directory
WORKDIR ./app
# Install app dependencies
COPY requirements.txt .

# env FLASK_APP=theflaskapp.py python -m flask run


RUN  python -m pip install --upgrade pip

RUN  pip install -r requirements.txt


# Bundle app source
COPY . ./app
ENV FLASK_APP=run.py

EXPOSE 5000
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]