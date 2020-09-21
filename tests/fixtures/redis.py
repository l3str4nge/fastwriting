import pytest

from src.redis.interface import get_redis


@pytest.mark.asyncio
@pytest.fixture()
async def redis_instance():
    return await get_redis()


@pytest.mark.asyncio
@pytest.fixture()
async def redis_with_game(redis_instance):
    await redis_instance.hset("test_game", "started", "")
    return redis_instance