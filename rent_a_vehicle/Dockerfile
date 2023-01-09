FROM python:3.10.7-alpine3.15
LABEL maintainer="rent-a-vehicle.com"

ENV PYTHONUNBUFFERED 1

COPY ./ /app

WORKDIR /app
EXPOSE 8000

RUN python -m venv /py && \
    /py/bin/pip install --upgrade  pip && \
    apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .temp-deps \
        build-base postgresql-dev musl-dev && \
    /py/bin/pip install -r /app/requirements.txt && \
    apk del .temp-deps && \
    adduser --disabled-password --no-create-home app && \
    mkdir -p /vol/web/media && \
    chown -R app:app /vol && \
    chown -R 755 /vol

ENV PATH="/py/bin:$PATH"

USER app
