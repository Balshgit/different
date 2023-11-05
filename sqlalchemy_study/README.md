# SQLALCHEMY v2 queries STUDY

---

*Note: MySQL will start on 3307 port*

*Note: Postgres will start on 5433 port*

---

## Create environment:

```bash
cp ./src/config/.env.template ./src/config/.env
```

*Note: Change USE_DATABASE variable to 'mysql' for MySQL training or 'postgres' for Postgres use.*

*Default is Postgres*

## Run without app in docker:

Requires python >= 3.11 and poetry >= 1.3.1

- **install poetry dependencies:**
```bash
poetry install
poetry shell
```

- **run for mysql:** ```docker compose -f docker-compose.mysql.yaml up```

- **run for postgres:** ```docker compose -f docker-compose.postgres.yaml up```

- **run initial data:** 
```bash
cd src
python /data/fill_data.py
```

## Run all in docker:

**run for mysql:**
```bash
docker compose -f docker-compose.mysql.yaml -f docker-compose.docker.yaml up
```
**run for postgres:**
```bash
docker compose -f docker-compose.postgres.yaml -f docker-compose.docker.yaml up
```
*Note: docker will start all migrations automatically. You don't need creation data step*

## Help info:

### Create alembic migrations:

*Note: To generate migrations you should run:*
```bash
# For automatic change detection.
alembic revision --autogenerate -m "migration message"

# For empty file generation.
alembic revision
```

*Note: If you want to migrate your database, you should run following commands:*
```bash
# To run all migrations untill the migration with revision_id.
alembic upgrade "<revision_id>"

# To perform all pending migrations.
alembic upgrade "head"
```

### Reverting alembic migrations:

*Note: If you want to revert migrations, you should run:*
```bash
# revert all migrations up to: revision_id.
alembic downgrade <revision_id>

# Revert everything.
alembic downgrade base
 
# Revert N revisions.
alembic downgrade -2
```

### MySQL database access:

Postgres:
```bash
docker exec -it sqlalchemy_study_db psql -d sqlalchemy_study -U balsh
```

- show help ```\?```
- show all tables: ```\dt```
- describe table ```\d {table name}```



## Clean database
```bash
docker compose -f docker-compose.mysql.yaml down -v
docker compose -f docker-compose.postgres.yaml down -v
```

## Known issues:
