from data.fill_data import fill_database
from db.utils import drop_tables, run_migrations

if __name__ == "__main__":
    drop_tables()
    run_migrations()
    fill_database()
