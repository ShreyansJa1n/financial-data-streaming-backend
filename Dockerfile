FROM python:3.11-slim-buster

WORKDIR /app
COPY ./app /app
COPY ./scripts /app/scripts
COPY ./requirements/requirements.txt /app/requirements/requirements.txt
COPY ./wait-for-postgres.sh /wait-for-postgres.sh
COPY ./wait-for-kafka.sh /wait-for-kafka.sh
# RUN apk add --no-cache build-base
RUN apt-get update && apt-get install -y build-essential
RUN chmod +x /wait-for-postgres.sh
# Install nc
RUN apt-get install -y netcat
RUN chmod +x /wait-for-kafka.sh
# Install psql
# RUN apk add --no-cache postgresql-client
RUN apt-get update && apt-get install -y postgresql-client
#Install librdkafka v2.10.1
# RUN apk add --no-cache librdkafka-dev
RUN apt-get install -y librdkafka-dev
# Install Python dependencies
RUN ls ./scripts && cd ./scripts && \
    make install_dependencies