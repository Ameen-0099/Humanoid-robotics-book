from .database import engine
from .models.user import Base # Import Base from user models

def init_db():
    Base.metadata.drop_all(bind=engine) # Explicitly drop all tables
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()