# Python
FROM python:3.8-slim

ENV PYTHONUNBUFFERED 1
WORKDIR /Timer

RUN apt-get update -y
RUN apt-get upgrade -y
RUN apt-get install -y apt-utils
RUN apt-get install gcc -y
RUN apt-get clean
RUN apt-get install -y python-setuptools
RUN apt-get install -y libpq-dev python3-dev
RUN apt-get install -y systemd
RUN apt-get install nmap -y


COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . ./Timer

EXPOSE 8000

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8080" ]

# Redis-Server
#FROM redis:6.2.1-alpine
#
#EXPOSE 6379
#CMD [ "redis-server", "--port", "6379" ]
#
## Celery
#FROM celery:4.0.2
#EXPOSE 5672


