from app.database import engine
from app import models

print("creating dataset...")
models.Base.metadata.create_all(bind=engine)
print("dataset initialization done, file created")
