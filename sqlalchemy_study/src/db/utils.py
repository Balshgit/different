from alembic import command, config as alembic_config
from sqlalchemy_study.sqlalchemy import MetaData, Table, ForeignKeyConstraint
from sqlalchemy_study.sqlalchemy import inspect
from sqlalchemy_study.sqlalchemy import NoSuchTableError
from sqlalchemy_study.sqlalchemy import DropConstraint

from db.dependencies import sync_engine
from db.meta import meta
from db.models import load_all_models
from settings import settings
from settings.logger import logger

alembic_cfg = alembic_config.Config("alembic.ini")


def remove_foreign_keys() -> None:
    logger.info("Dropping all foreign key constraints from archive database")

    inspector = inspect(sync_engine)
    fake_metadata = MetaData()

    fake_tables = []
    all_fks = []
    for table_name in meta.tables:
        fks = []
        try:
            for fk in inspector.get_foreign_keys(table_name):
                if fk['name']:
                    fks.append(ForeignKeyConstraint((), (), name=fk['name']))
        except NoSuchTableError:
            logger.error(f'Table {table_name} not exist')
        t = Table(table_name, fake_metadata, *fks)
        fake_tables.append(t)
        all_fks.extend(fks)
    connection = sync_engine.connect()
    transaction = connection.begin()
    for fkc in all_fks:
        connection.execute(DropConstraint(fkc))
    transaction.commit()


def drop_tables() -> None:
    load_all_models()
    remove_foreign_keys()
    meta.drop_all(bind=sync_engine, checkfirst=True)
    sync_engine.execute('DROP TABLE IF EXISTS alembic_version')
    sync_engine.dispose()
    logger.info("All tables are dropped")


def run_migrations() -> None:
    with sync_engine.begin() as connection:
        alembic_cfg.attributes['connection'] = connection
        migration_dialect = 'mysql_init_migrations' if settings.USE_DATABASE == 'mysql' else 'postgres_init_migrations'
        command.upgrade(alembic_cfg, migration_dialect)
    logger.info('Tables recreated')
