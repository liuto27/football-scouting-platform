from database.db import engine, Base, SessionLocal
from database import models


def reset_all():
    print("Dropping ALL tables...")
    Base.metadata.drop_all(bind=engine)
    print("Recreating ALL tables...")
    Base.metadata.create_all(bind=engine)
    print("Done resetting entire database.")


def reset_tables(table_names):
    print(f"Resetting tables: {table_names}")

    # Map table names to actual SQLAlchemy Table objects
    metadata_tables = Base.metadata.tables

    # Drop selected tables
    for name in table_names:
        if name in metadata_tables:
            print(f"Dropping table: {name}")
            metadata_tables[name].drop(engine, checkfirst=True)
        else:
            print(f"Table not found: {name}")

    # Recreate selected tables
    for name in table_names:
        if name in metadata_tables:
            print(f"Recreating table: {name}")
            metadata_tables[name].create(engine, checkfirst=True)

    print("Done resetting selected tables.")


if __name__ == "__main__":
    # Examples:
    # reset_all()
    # reset_tables(["players", "teams"])

    reset_all()
