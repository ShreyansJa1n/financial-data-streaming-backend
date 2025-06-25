from fastapi import FastAPI
from app.api.api import api_router
from app.services.Redis import RedisService
from app.core.Database import engine
import app.models.market as market
from app.core.config import settings
from contextlib import asynccontextmanager
from sqlalchemy import inspect
from app.core.logging import logger as logging
from app.services.kafka.ma_consumer_runner import PriceEventConsumer
from app.services.PollingService import PollingService
import asyncio
import threading

from confluent_kafka.admin import AdminClient, NewTopic

# Initialize Redis service
redis_service = RedisService()
consumer_svc = PriceEventConsumer()

def run_consumer():
    async def async_consume():
        await consumer_svc.start_ma_consumer()
                
    asyncio.run(async_consume())

@asynccontextmanager
async def lifespan(app):
    # Store redis_service in app state
    logging.info("Connecting to Redis...")
    app.state.redis_service = redis_service
    await redis_service.connect()
    logging.info("Creating database tables...")
    try:
        async with engine.begin() as conn:
            await conn.run_sync(market.Base.metadata.create_all)

            def get_tables(sync_conn):
                inspector = inspect(sync_conn)
                return inspector.get_table_names()

            tables = await conn.run_sync(get_tables)
        logging.info("Tables created successfully!")
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
    consumer_thread = threading.Thread(target=run_consumer, daemon=True)
    consumer_thread.start()

    logging.info("Starting Polling Service")
    polling_svc = PollingService()
    polling_task = asyncio.create_task(polling_svc.start_polling())
    app.state.polling_task = polling_task



    yield
    await redis_service.disconnect()
    logging.info("Stopping price event consumer...")
    consumer_svc.stop_ma_consumer()

    polling_svc.stop_polling()
    await polling_task


app = FastAPI(lifespan=lifespan)

app.include_router(api_router)
