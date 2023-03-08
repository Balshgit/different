#!/bin/bash

TIMEOUT=${TIMEOUT:-60}

DATABASE_HOST=${DB_HOST:-db_host}

POSTGRES_DATABASE_PORT=${POSTGRES_DB_PORT:-5432}
POSTGRES_DATABASE="$DATABASE_HOST:$POSTGRES_DATABASE_PORT"

MYSQL_DATABASE_PORT=${MYSQL_DB_PORT:-3306}
MYSQL_DATABASE="$DATABASE_HOST:$MYSQL_DATABASE_PORT"

wait_for_databases(){
  echo "Chosen database IS $USE_DATABASE"
  if [ "$USE_DATABASE" = "mysql" ];
    then
      echo "Waiting for DB on: $MYSQL_DATABASE"
      /app/scripts/wait-for-it.sh -t $TIMEOUT -s $MYSQL_DATABASE -- echo 'MySQL database connected';
  elif [ "$USE_DATABASE" = "postgres" ];
    then
      echo "Waiting for DB on: $POSTGRES_DATABASE"
      /app/scripts/wait-for-it.sh -t $TIMEOUT -s $POSTGRES_DATABASE -- echo 'Postgres database connected';
  fi
}

wait_for_databases