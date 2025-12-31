from database.db import Base, engine
from database import models

print("Creating database...")
Base.metadata.create_all(bind=engine)
print("Done.")
