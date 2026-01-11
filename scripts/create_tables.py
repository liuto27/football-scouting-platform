from database.db import engine, Base
from database import models

print("Creating all tables...")
Base.metadata.create_all(bind=engine)
print("Done.")
