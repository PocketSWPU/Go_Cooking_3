from sqlmodel import create_engine, SQLModel
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import sys
import os
# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.models import Dish, Ingredient, DishIngredientLink, DishHistory

# Load environment variables from .env file in the backend directory
env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')
load_dotenv(env_path)

def get_database_url(environment=None):
    """Get database URL based on the environment parameter."""
    # Determine which environment to use, default to 'dev'
    # First check if environment is provided as parameter, otherwise fall back to environment variable
    if environment is None:
        ENV = os.getenv("ENV", "dev")
    else:
        ENV = environment

    # Base database connection parameters (same for all environments)
    DB_USER = "postgres"
    DB_PASSWORD = "299793"
    DB_HOST = "localhost"
    DB_PORT = "5432"

    # Select database name based on environment
    if ENV.lower() in ["prod", "production"]:
        DB_NAME = os.getenv("PROD_DATABASE_NAME", "go_cooking_3_product")
    else:  # default to dev environment
        DB_NAME = os.getenv("DEV_DATABASE_NAME", "go_cooking_3_dev")

    # Construct the database URL
    DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    print(f"Using environment: {ENV}")
    print(f"Connecting to database: {DATABASE_URL}")

    return DATABASE_URL, ENV

# Global variables that will be initialized when needed
DATABASE_URL = None
ENV = None
engine = None
SessionLocal = None

def init_db_engine(environment=None):
    """Initialize the database engine with the specified environment."""
    global engine, SessionLocal, DATABASE_URL, ENV
    DATABASE_URL, ENV = get_database_url(environment)
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return engine

# Don't auto-initialize - only initialize when explicitly called with environment parameter

def create_db_and_tables():
    """
    Automatically create all tables based on SQLModel entity relationships.
    This function will create tables for all SQLModel classes that have table=True.
    """
    global engine
    # Initialize engine if not already done (with default dev environment)
    if engine is None:
        init_db_engine()
    print("Registered tables:", list(SQLModel.metadata.tables.keys()))
    SQLModel.metadata.create_all(engine)


def get_db():
    global SessionLocal
    # Initialize SessionLocal if not already done (with default dev environment)
    if SessionLocal is None:
        init_db_engine()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()