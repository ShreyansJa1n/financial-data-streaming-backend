FROM python:3.11-alpine3.22

WORKDIR /app
COPY ./app /app
COPY ./scripts /app/scripts
COPY ./requirements/requirements.txt /app/requirements/requirements.txt
RUN apk add --no-cache build-base
RUN ls ./scripts && cd ./scripts && \
    make install_dependencies