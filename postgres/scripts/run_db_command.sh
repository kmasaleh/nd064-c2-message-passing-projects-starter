psql -U $POSTGRES_USER -d $POSTGRES_DB -a -f /app/scripts/2020-08-15_init-db.sql
psql -U $POSTGRES_USER -d $POSTGRES_DB -a -f /app/scripts/udaconnect_public_person.sql
psql -U $POSTGRES_USER -d $POSTGRES_DB -a -f /app/scripts/udaconnect_public_location.sql
