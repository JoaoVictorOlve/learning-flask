FROM python:3.8.10

WORKDIR /app

ADD . /app

RUN pip install -r requirements.txt

CMD["uwsgi", "app.ini"]