from sqlmodel import create_engine, SQLModel
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import sys
import os
# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.models import Dish, Ingredient, DishIngredientLink

# Load environment variables from .env file in the backend directory
env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')
load_dotenv(env_path)

# Determine which environment to use, default to 'dev'
ENV = os.getenv("ENV", "dev")

# Base database connection parameters (same for all environments)
DB_USER = "postgres"
DB_PASSWORD = "299793"
DB_HOST = "localhost"
DB_PORT = "5432"

# Select database name based on environment
if ENV.lower() == "prod" or ENV.lower() == "production":
    DB_NAME = os.getenv("PROD_DATABASE_NAME", "go_cooking_3_prod")
else:  # default to dev environment
    DB_NAME = os.getenv("DEV_DATABASE_NAME", "go_cooking_3_dev")

# Construct the database URL
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

print(f"Using environment: {ENV}")
print(f"Connecting to database: {DATABASE_URL}")

engine = create_engine(DATABASE_URL)


def create_db_and_tables():
    """
    Automatically create all tables based on SQLModel entity relationships.
    This function will create tables for all SQLModel classes that have table=True.
    """
    print("Registered tables:", list(SQLModel.metadata.tables.keys()))
    SQLModel.metadata.create_all(engine)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()