from fastapi import FastAPI
from app.api.api import api_router
from app.services.Redis import RedisService
# Initialize Redis service
redis_service = RedisService()

# Connect to Redis
async def connect_redis():
    await redis_service.connect()
# Disconnect from Redis on shutdown
async def disconnect_redis():
    await redis_service.disconnect()

app = FastAPI()

# Store redis_service in app state
app.state.redis_service = redis_service

app.add_event_handler("startup", connect_redis)
app.add_event_handler("shutdown", disconnect_redis)



app.include_router(api_router)
