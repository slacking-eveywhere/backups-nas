FROM python:3.10-slim as dev

WORKDIR /app

COPY . .
COPY requirements.txt requirements.txt

RUN apt-get update ; \
    apt-get upgrade ; \
    apt-get install -y \
        git 

RUN python -m pip install -r requirements.txt


FROM dev as exec