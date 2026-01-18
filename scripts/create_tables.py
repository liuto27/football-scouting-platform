from database.db import engine, Base

print("Creating all tables...")
Base.metadata.create_all(bind=engine)
print("Done.")
