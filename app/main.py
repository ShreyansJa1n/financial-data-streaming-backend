from fastapi import FastAPI
from app.api.api import api_router
from app.services.Redis import RedisService
from app.services.Database import engine
import app.models as models
from app.core.config import settings
from contextlib import asynccontextmanager
from sqlalchemy import inspect
from app.core.logging import logging

from confluent_kafka.admin import AdminClient, NewTopic

# Initialize Redis service
redis_service = RedisService()


@asynccontextmanager
async def lifespan(app):
    # Store redis_service in app state
    logging.info("Connecting to Redis...")
    app.state.redis_service = redis_service
    await redis_service.connect()
    logging.info("Creating database tables...")
    try:
        models.Base.metadata.create_all(bind=engine)
        logging.info("Tables created successfully!")
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        logging.info(f"Tables in database: {tables}")
    except Exception as e:
        logging.error(f"Error creating tables: {e}")

    logging.info("Creating Kafka topics...")
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
                logging.info(f"Topic {topic} created successfully.")
            except Exception as e:
                logging.error(f"Failed to create topic {topic}: {e}")
        
    except Exception as e:
        logging.error(f"Kafka AdminClient setup failed: {e}")
    else:
        logging.info("Kafka topics created successfully.")

    logging.info("Starting price event consumer...")
    #TODO: Implement the actual consumer logic

    yield
    await redis_service.disconnect()
    logging.info("Stopping price event consumer...")
    #TODO: Implement the actual consumer shutdown logic


app = FastAPI(lifespan=lifespan)

app.include_router(api_router)
