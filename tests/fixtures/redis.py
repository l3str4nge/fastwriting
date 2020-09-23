import pytest

from src.redis.interface import get_redis


@pytest.mark.asyncio
@pytest.fixture()
async def redis_instance():
    r = await get_redis()
    yield r
    await r.redis_instance.flushall(async_op=True)
    await r.redis_instance.flushdb(async_op=True)


@pytest.mark.asyncio
@pytest.fixture()
async def redis_with_game(redis_instance):
    await redis_instance.hset("test_game_x", "started", "")
    yield redis_instance

