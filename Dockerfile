# pull official base image
FROM python:3.7.4-alpine

# set work directory
WORKDIR /usr/src/

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk add --no-cache --virtual .build-deps gcc musl-dev

# install python-dev
RUN apk update \
    && apk add --virtual .build-deps gcc libc-dev libxslt-dev \
    && apk add libffi-dev openssl-dev linux-headers \
    && apk add --no-cache libxslt \
    && pip install lxml==4.5.0

# install psycopg2
RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add postgresql-dev \
    && pip install psycopg2 \
    && pip install --upgrade incremental

# install zlib for pillow
RUN apk add --no-cache jpeg-dev zlib-dev build-base

# install dependencies
RUN pip install --upgrade pip setuptools

# copy requirements
COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt
RUN pip install gunicorn==20.0.4

WORKDIR /usr/src/app/

# copy entrypoint-prod.sh
COPY ./entrypoint.prod.sh ./entrypoint.prod.sh

ADD ["./karsoogh", "./karsoogh"]
ADD ["./problembank", "./problembank"]
ADD ["./Game", "./Game"]
ADD ["./Account", "./Account"]
COPY ./manage.py ./manage.py


RUN adduser -D game_backend

RUN mkdir -p mkdir -p /usr/src/app/staticfiles && chown -R game_backend /usr/src/app/staticfiles \
        && mkdir -p /usr/src/app/media && chown -R game_backend /usr/src/app/media

RUN chown -R game_backend /usr/src/app/

USER game_backend

# run entrypoint.prod.sh
ENTRYPOINT ["/usr/src/app/entrypoint.prod.sh"]
