# pull official base image
FROM python:3.6-alpine

# set work directory
WORKDIR /usr/src/app

# set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ARG OPENCV_VERSION=3.4.2

# install psycopg2
#RUN apk update \
#    && apk add --virtual build-deps gcc python3-dev musl-dev \
#    && apk add postgresql-dev \
#    && apk del build-deps
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

ENV LANG=C.UTF-8

# install dependencies
RUN pip install --upgrade pip
COPY requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

# copy project
COPY . /usr/src/app/


# run entrypoint.sh
ENTRYPOINT ["/usr/src/app/business-logic-server/entrypoint.sh"]