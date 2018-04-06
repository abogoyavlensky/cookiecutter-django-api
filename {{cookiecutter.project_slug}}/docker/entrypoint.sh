#!/bin/sh
set -e

cmd="$@"

function db_ready(){
python << END
import sys
import psycopg2
import environ
config = environ.Env().db('DATABASE_URL')
try:
    conn = psycopg2.connect(dbname=config['NAME'], user=config['USER'], password=config['PASSWORD'], host=config['HOST'], port=config['PORT'])
except psycopg2.OperationalError:
    sys.exit(-1)
sys.exit(0)
END
}

until db_ready; do
>&2 echo "PostgreSQL is unavailable - sleeping"
sleep 1
done

>&2 echo "PostgreSQL is up - continuing..."
exec $cmd
