FROM python:3.8-slim

RUN apt update && \
    mkdir /app

WORKDIR /app

ADD ./requirements.txt /app/requirements.txt
RUN pip --no-cache-dir install -r requirements.txt

COPY ./src /app
