import pytest
from unittest.mock import patch

from src.game.game import Game, Stage
from tests.fixtures.redis import redis_instance, redis_with_game
from tests.fixtures.db import session, db
from src.services import new_game, create_stage


@pytest.mark.asyncio
async def test_create_new_game():
    game_obj = await new_game("test_username")

    assert game_obj
    assert game_obj['started']
    assert game_obj['current_stage'] == 1


@pytest.mark.asyncio
async def test_get_game_from_redis(redis_instance):
    await redis_instance.hmset("TEST_GAME", **{"username": "username", "started": "2020-12-12", "current_stage": 1})
    game = await Game.from_redis("TEST_GAME")

    assert game["username"] == "username"
    assert game["started"] == "2020-12-12"
    assert game["current_stage"] == "1"


@pytest.mark.asyncio
@patch('src.database.base.SessionLocal')
@patch('src.game.game.query_random_words')
async def test_create_first_stage(random_words, mock_session):
    random_words.return_value = ','.join(["TEST" for _ in range(60)])
    stage = await create_stage(mock_session, "test_game_x", stage=1)

    assert stage['number'] == 1
    assert stage['timeout'] == 120
    assert len(stage['words'].split(',')) == 60

@pytest.mark.asyncio
async def test_create_get_stage_from_redis(redis_instance):
    await redis_instance.hmset("STAGE_ID", **{"game_id": "123", "number": 1, "words": "test,test", "timeout": 60})
    stage = await Stage.from_redis("STAGE_ID")

    assert stage['game_id'] == '123'