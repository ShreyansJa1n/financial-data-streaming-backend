FROM python:3.11-alpine3.22

WORKDIR /app
COPY ./app /app
COPY ./scripts /app/scripts
COPY ./requirements/requirements.txt /app/requirements/requirements.txt
COPY ./wait-for-postgres.sh /wait-for-postgres.sh
RUN apk add --no-cache build-base
RUN chmod +x /wait-for-postgres.sh
# Install psql
RUN apk add --no-cache postgresql-client
RUN ls ./scripts && cd ./scripts && \
    make install_dependencies