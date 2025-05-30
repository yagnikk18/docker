from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Get the database URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL")

# Create the SQLAlchemy engine
# This engine manages the database connection pool and issues SQL statements
engine = create_engine(DATABASE_URL)

# Create a configured "Session" class
# SessionLocal will be used to create individual session instances
SessionLocal = sessionmaker(bind=engine)

# Base class for all ORM models
# All models should inherit from this Base to enable table creation and reflection
Base = declarative_base()
