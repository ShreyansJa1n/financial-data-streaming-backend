from fastapi import FastAPI
from app.api.api import api_router
from app.services.Redis import RedisService
from app.services.Database import engine, get_db
import app.models as models
from contextlib import asynccontextmanager

# Initialize Redis service
redis_service = RedisService()

@asynccontextmanager
async def lifespan(app):
    # Store redis_service in app state
    print("Connecting to Redis...")
    app.state.redis_service = redis_service
    await redis_service.connect()
    print("Creating database tables...")
    try:
        models.Base.metadata.create_all(bind=engine)
        print("Tables created successfully!")
        from sqlalchemy import inspect
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        print(f"Tables in database: {tables}")
    except Exception as e:
        print(f"Error creating tables: {e}")
    yield
    await redis_service.disconnect()

app = FastAPI(lifespan=lifespan)

app.include_router(api_router)
