# Database initialization script
# This script will automatically create all tables based on the entity relationships defined in models.py

import os
import argparse

def set_environment(env=None):
    """Set the environment based on parameter, command line arguments, or default to dev"""
    if env is not None:
        # Use the environment passed as parameter
        os.environ['ENV'] = env
        print(f"Selected environment: {env}")
    elif __name__ == "__main__":
        # Only parse arguments if running as main script
        parser = argparse.ArgumentParser(description='Initialize GoCooking 3 Database')
        parser.add_argument('--env', '-e', type=str, default='dev',
                            choices=['dev', 'development', 'prod', 'production'],
                            help='Environment to run the initialization (default: dev)')

        # Parse only known args to avoid conflicts
        args, _ = parser.parse_known_args()

        # Set environment variable for database connection
        os.environ['ENV'] = args.env
        print(f"Selected environment: {args.env}")
    else:
        # For imports, use the existing environment or default to dev
        if 'ENV' not in os.environ:
            os.environ['ENV'] = 'dev'

from backend.database import create_db_and_tables

def init_db(env=None):
    """
    Initialize database tables
    :param env: Environment to use ('dev', 'prod', etc.). If None, uses default or ENV variable
    """
    set_environment(env)
    # Create all tables based on entity relationships
    create_db_and_tables()
    print(f"Database tables created successfully in {env or os.getenv('ENV', 'dev')} environment!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Initialize GoCooking 3 Database')
    parser.add_argument('--env', '-e', type=str, default='dev',
                        choices=['dev', 'development', 'prod', 'production'],
                        help='Environment to run the initialization (default: dev)')
    args = parser.parse_args()
    init_db(args.env)