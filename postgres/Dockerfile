FROM postgres:12 as postgresdb
WORKDIR /app
COPY ./scripts/run_db_command.sh /docker-entrypoint-initdb.d
COPY ./scripts/2020-08-15_init-db.sql /2020-08-15_init-db.sql
COPY ./scripts/udaconnect_public_person.sql /udaconnect_public_person.sql
COPY ./scripts/udaconnect_public_location.sql /udaconnect_public_location.sql
