import redis.asyncio as redis
import json
import hashlib
from typing import Any, Optional
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)


class RedisService:
    def __init__(self):
        self.redis: Optional[redis.Redis] = None
        self.is_connected = False

    async def connect(self):
        if not self.is_connected:
            try:
                self.redis = redis.from_url(
                    settings.REDIS_URL,
                    decode_responses=True,
                    socket_connect_timeout=5,
                    retry_on_timeout=True,
                    health_check_interval=30,
                )
                await self.redis.ping()
                self.is_connected = True
                logger.info("Connected to Redis")
            except redis.ConnectionError as e:
                logger.error(f"Failed to connect to Redis: {e}")
                raise e
        return self.redis
    
    async def disconnect(self):
        if self.redis:
            try:
                await self.redis.close()
                self.is_connected = False
                logger.info("Disconnected from Redis")
            except redis.ConnectionError as e:
                logger.error(f"Failed to disconnect from Redis: {e}")
                raise e
            
    async def health_check(self) -> bool:
        if not self.is_connected:
            return False
        try:
            await self.redis.ping()
            return True
        except redis.ConnectionError:
            return False
        
        
    def __serialize__(self, data: Any) -> str:
        """Serialize data to JSON string."""
        return json.dumps(data, default=str)
    
    def __deserialize__(self, data: str) -> Any:
        """Deserialize JSON string to Python object."""
        return json.loads(data)
    
    def __generate_key(self, key: str) -> str:
        """Generate a consistent key for Redis storage."""
        return hashlib.sha256(key.encode()).hexdigest()
    
    async def set(self, key: str, value: Any, expire: int = 60) -> bool:
        """Set a value in Redis with an optional expiration time."""
        if not self.redis:
            raise ConnectionError("Redis connection is not established.")
        
        serialized_value = self.__serialize__(value)
        redis_key = self.__generate_key(key)
        
        try:
            await self.redis.set(redis_key, serialized_value, ex=expire)
            return True
        except redis.RedisError as e:
            logger.error(f"Failed to set key {key} in Redis: {e}")
            return False
        
    async def get(self, key: str) -> Optional[Any]:
        """Get a value from Redis."""
        if not self.redis:
            raise ConnectionError("Redis connection is not established.")
        
        redis_key = self.__generate_key(key)
        
        try:
            value = await self.redis.get(redis_key)
            if value is None:
                return None
            return self.__deserialize__(value)
        except redis.RedisError as e:
            logger.error(f"Failed to get key {key} from Redis: {e}")
            return None
        
    async def exists(self, key: str) -> bool:
        """Check if a key exists in Redis."""
        if not self.redis:
            raise ConnectionError("Redis connection is not established.")
        
        redis_key = self.__generate_key(key)
        
        try:
            return await self.redis.exists(redis_key) > 0
        except redis.RedisError as e:
            logger.error(f"Failed to check existence of key {key} in Redis: {e}")
            return False
        
    async def delete(self, key: str) -> bool:
        """Delete a key from Redis."""
        if not self.redis:
            raise ConnectionError("Redis connection is not established.")
        
        redis_key = self.__generate_key(key)
        
        try:
            result = await self.redis.delete(redis_key)
            return result > 0
        except redis.RedisError as e:
            logger.error(f"Failed to delete key {key} from Redis: {e}")
            return False
