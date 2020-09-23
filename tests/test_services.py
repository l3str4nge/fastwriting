import pytest
from unittest.mock import patch
from tests.fixtures.redis import redis_instance, redis_with_game
from tests.fixtures.db import session, db
from src.services import new_game, create_level


@pytest.mark.asyncio
async def test_create_new_game(redis_instance):
    game_obj = await new_game("test_username")

    assert game_obj
    assert game_obj['started']
    assert game_obj['current_stage'] == 1
    # TODO: more tests if game hash will be bigger


@pytest.mark.asyncio
@patch('src.database.base.SessionLocal')
@patch('src.services.query_random_words')
async def test_create_first_level(random_words, mock_session, redis_with_game):
    random_words.return_value = ','.join(["TEST" for _ in range(60)])
    await create_level(mock_session, "test_game_x", stage=1)
    level_obj = await redis_with_game.hgetall("test_game_x")

    assert level_obj['stage'] == '1'
    assert level_obj['timeout'] == '120'
    assert len(level_obj['words'].split(',')) == 60
