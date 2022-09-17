FROM python:3.7-alpine

WORKDIR /modules

RUN apk add --no-cache gcc musl-dev linux-headers geos libc-dev postgresql-dev

RUN mkdir -p -v shared
RUN mkdir -p -v gRpcPersons
COPY ./shared shared
COPY ./gRpcPersons gRpcPersons

RUN pip install --upgrade pip
RUN pip install protobuf
RUN pip install grpcio
RUN pip install ez_setup 
RUN pip install -r ./shared/requirements.txt

ENV GRPC_PERSONS_API_SERVICE_HOST  "host.docker.internal"
ENV HTTP_CONNECTIONS_API_SERVICE_HOST  "host.docker.internal"
ENV KAFKA_SERVICE_SERVICE_HOST "host.docker.internal"
ENV DB_USERNAME  "ct_admin"
ENV DB_PASSWORD  "d293aW1zb3NlY3VyZQ=="
ENV DB_HOST   "host.docker.internal"
ENV DB_PORT  "5432"
ENV DB_NAME  "geoconnections"

EXPOSE 5006
CMD ["python","./gRpcPersons/main.py"]