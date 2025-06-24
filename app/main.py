from fastapi import FastAPI
from app.api.api import api_router
from app.services.Redis import RedisService
from app.services.Database import engine
import app.models as models
from app.core.config import settings
from contextlib import asynccontextmanager
from sqlalchemy import inspect

from confluent_kafka.admin import AdminClient, NewTopic

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
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        print(f"Tables in database: {tables}")
    except Exception as e:
        print(f"Error creating tables: {e}")

    print("Creating Kafka topics...")
    try:
        kafka_admin_client = AdminClient(
            {
                "bootstrap.servers": settings.KAFKA_BOOTSTRAP_SERVERS,
            }
        )
        new_topics = [
            NewTopic("price_events", 1, 1),
        ]
        fs = kafka_admin_client.create_topics(new_topics, validate_only=False)
        for topic, f in fs.items():
            try:
                f.result(timeout=5)  # Wait for topic creation with timeout
                print(f"Topic {topic} created successfully.")
            except Exception as e:
                print(f"Failed to create topic {topic}: {e}")
        
    except Exception as e:
        print(f"Kafka AdminClient setup failed: {e}")
    else:
        print("Kafka topics created successfully.")

    print("Starting price event consumer...")
    #TODO: Implement the actual consumer logic

    yield
    await redis_service.disconnect()
    print("Stopping price event consumer...")
    #TODO: Implement the actual consumer shutdown logic


app = FastAPI(lifespan=lifespan)

app.include_router(api_router)
