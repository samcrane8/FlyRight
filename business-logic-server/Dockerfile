# pull official base image
FROM ubuntu:bionic

# set work directory
WORKDIR /usr/src/app

# set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update -qq && apt-get install -y -qq \
    # std libs
    unzip wget sudo less nano curl git gosu build-essential software-properties-common \
    # python basic libs
    python3.7 python3.7-dev gettext \
    # geodjango
    gdal-bin binutils libproj-dev libgdal-dev \
    netcat \
    # postgresql
    libpq-dev postgresql-client && \
    apt-get clean all && rm -rf /var/apt/lists/* && rm -rf /var/cache/apt/*

# install pip
RUN wget https://bootstrap.pypa.io/get-pip.py && python3.7 get-pip.py && rm get-pip.py
RUN pip3 install --no-cache-dir setuptools wheel -U

ENV LANG=C.UTF-8

# install dependencies
RUN pip3 install --upgrade pip
COPY requirements.txt /usr/src/app/requirements.txt
RUN pip3 install -r requirements.txt

# copy project
COPY . /usr/src/app/


# run entrypoint.sh
ENTRYPOINT ["/usr/src/app/business-logic-server/entrypoint.sh"]