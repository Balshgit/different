#!/bin/bash

alembic_init_migrations(){
  echo "Chosen database IS $USE_DATABASE"
  if [ "$USE_DATABASE" = "mysql" ];
    then
      echo "Start migrations for MySQL"
      alembic upgrade mysql_init_migrations;
  elif [ "$USE_DATABASE" = "postgres" ];
    then
      echo "Start migrations for Postgres"
      alembic upgrade postgres_init_migrations;
  fi
}

alembic_init_migrations