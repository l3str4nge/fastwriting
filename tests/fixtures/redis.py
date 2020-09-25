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


@pytest.mark.asyncio
@pytest.fixture()
async def redis_with_stage(redis_instance):
    # TODO: maybe faker-boy would fit in here?
    # https://github.com/FactoryBoy/factory_boy
    await redis_instance.hmset("test_stage", **{
        "game_id": '123',
        "number": 1,
        "words": 'test,test',
        "timeout": 120,
        "score": 0
    })

    yield redis_instance

