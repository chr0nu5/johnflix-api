FROM python:3.9.10
LABEL maintainer John <john@fehra.co>

ENV PYTHONUNBUFFERED 1

RUN apt-get update -y
RUN apt-get install build-essential -y
RUN apt-get install ffmpeg -y
RUN apt-get install libmagic1 -y
RUN apt-get install libpq-dev -y
RUN apt-get install python3-dev -y

RUN pip install boto3==1.34.77
RUN pip install coverage==7.4.4
RUN pip install django-jazzmin==3.0.0
RUN pip install django==4.2.11
RUN pip install djangorestframework==3.15.1
RUN pip install moviepy==1.0.3
RUN pip install mutagen==1.46.0
RUN pip install pep8==1.7.1
RUN pip install psycopg2==2.8.6
RUN pip install python-magic==0.4.26
RUN pip install pytz==2024.1
RUN pip install requests==2.31.0

RUN mkdir /app

WORKDIR /app

COPY . /app

RUN coverage run --omit=/app/manage.py manage.py test && coverage report -m
RUN python /app/coverage.py

ENTRYPOINT ["/app/entrypoint.sh"]