import aioredis as aioredis
from settings.settings import redis_server


async def get_redis():
    return await aioredis.create_redis_pool(f'redis://{redis_server}')

