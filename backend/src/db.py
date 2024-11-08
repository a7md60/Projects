from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Define database connection URL
DATABASE_URL = "postgresql://healt_bot:healt_bot@database/healt_bot"

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Create a sessionmaker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)