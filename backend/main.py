import os
import argparse
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

def set_environment():
    """Set the environment before importing database to ensure proper configuration"""
    # Only parse arguments if running as main script
    if __name__ == "__main__":
        parser = argparse.ArgumentParser(description='Start GoCooking 3 API')
        parser.add_argument('--env', '-e', type=str, default='dev',
                            choices=['dev', 'development', 'prod', 'production'],
                            help='Environment to run the application (default: dev)')

        # Parse only known args to avoid conflicts with uvicorn
        args, _ = parser.parse_known_args()

        # Set environment variable for database connection
        os.environ['ENV'] = args.env
        print(f"Selected environment: {args.env}")

        # Initialize database with the selected environment
        from backend.database import init_db_engine
        init_db_engine(args.env)
    else:
        # For imports, use the existing environment or default to dev
        if 'ENV' not in os.environ:
            os.environ['ENV'] = 'dev'

set_environment()

# Import routes after environment is set
from backend.routes.dish_routes import router as dish_router
from backend.routes.ingredient_routes import router as ingredient_router

app = FastAPI(title="GoCooking 3 API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(dish_router)
app.include_router(ingredient_router)

@app.get("/")
def read_root():
    env = os.getenv('ENV', 'dev')
    return {"message": f"Welcome to GoCooking 3 API", "environment": env}

if __name__ == "__main__":
    import uvicorn
    parser = argparse.ArgumentParser(description='Start GoCooking 3 API')
    parser.add_argument('--env', '-e', type=str, default='dev',
                        choices=['dev', 'development', 'prod', 'production'],
                        help='Environment to run the application (default: dev)')
    parser.add_argument('--host', type=str, default="0.0.0.0",
                        help='Host to run the application (default: 0.0.0.0)')
    parser.add_argument('--port', type=int, default=8000,
                        help='Port to run the application (default: 8000)')

    args = parser.parse_args()

    # Update environment if needed
    os.environ['ENV'] = args.env
    print(f"Starting server in {args.env} environment")

    # Initialize database with the selected environment
    from backend.database import init_db_engine
    init_db_engine(args.env)

    uvicorn.run(app, host=args.host, port=args.port)