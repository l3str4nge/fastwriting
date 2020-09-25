import aioredis as aioredis
from settings.settings import redis_server


async def get_redis():
    return await RedisInterface.get_instance()


class RedisInterface:
    redis_instance = None

    @classmethod
    async def get_instance(cls):
        cls.redis_instance = await aioredis.create_redis_pool(f'redis://{redis_server}')
        return cls

    @classmethod
    async def hmset(cls, key: str, **values):
        return await cls.redis_instance.hmset_dict(key, **values)

    @classmethod
    async def hset(cls, key, field, value):
        return await cls.redis_instance.hset(key, field, value)

    @classmethod
    async def hgetall(cls, key):
        return await cls.redis_instance.hgetall(key, encoding="utf-8")

    @classmethod
    async def hincrby(cls, key, field, value):
        return await cls.redis_instance.hincrby(key, field, value)