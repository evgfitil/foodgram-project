# Builder stage
FROM python:3.8.5-alpine as builder
LABEL stage=builder

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

RUN apk update \
    && apk add --virtual build-deps \
    && apk add gcc python3-dev musl-dev postgresql-dev \
    && apk add jpeg-dev zlib-dev libjpeg \
    && pip install Pillow

RUN pip install --upgrade pip
COPY . /usr/src/app/
COPY ./requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt

# Final stage
FROM python:3.8.5-alpine

RUN mkdir -p /home/app \
    && addgroup -S app && adduser -S app -G app

ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/static
RUN mkdir $APP_HOME/media
WORKDIR $APP_HOME

RUN apk update && apk add libpq \
    && set -ex && apk --no-cache add sudo
COPY --from=builder /usr/src/app/wheels /wheels
COPY --from=builder /usr/src/app/requirements.txt .
RUN chown -R app:app $APP_HOME
RUN chown -R app:app $HOME
RUN sudo -H pip install --upgrade pip
RUN sudo -H pip install --no-cache /wheels/*

COPY . $APP_HOME
RUN chown -R app:app $APP_HOME

USER app
RUN ./manage.py collectstatic --no-input
CMD gunicorn foodgram.wsgi:application --bind 0:8000