FROM python:3.6-alpine3.10
ENV PYTHONUNBUFFERED 1

RUN apk update

RUN apk add --no-cache postgresql-libs bash \
    && apk add --no-cache --virtual .build-deps \
    gcc musl-dev postgresql-dev \
    libffi-dev libressl-dev libxml2-dev libxslt-dev

WORKDIR /code

COPY ./requirements/* /code/requirements/

RUN pip install --upgrade pip && pip install -r requirements/dev.txt --no-cache-dir && apk del .build-deps

COPY . /code

EXPOSE 8000

ENTRYPOINT ["bash", "/code/docker-entrypoint.sh"]
