import pytest
from unittest.mock import patch

from src.game.game import Game, Stage
from tests.fixtures.redis import (
    redis_instance,
    redis_with_game,
    redis_with_stage
)
from tests.fixtures.db import session, db
from src.services import new_game, create_stage, pass_word_if_valid
from tests.utils.fakers import get_dummy_stage, get_dummy_game


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
    random_words.return_value = ["TEST" for _ in range(60)]
    stage = await create_stage(mock_session, "test_game_x", stage=1)
    assert stage['number'] == 1
    assert stage['timeout'] == 120
    assert len(stage['words'].split(',')) == 60


@pytest.mark.asyncio
async def test_create_get_stage_from_redis(redis_instance):
    await redis_instance.hmset("STAGE_ID", **{
        "game_id": "123",
        "number": 1,
        "words": "test,test",
        "timeout": 60,
        "score": 10
    })
    stage = await Stage.from_redis("STAGE_ID")

    assert stage.data['game_id'] == '123'
    assert stage.data['number'] == '1'
    assert stage.data['words'] == 'test,test'
    assert stage.data['timeout'] == '60'
    assert stage.data['score'] == 10


@pytest.mark.asyncio
@patch('src.services.Game.from_redis')
@patch('src.services.Stage.from_redis')
@patch('src.services.Stage.pass_word')
async def test_pass_word_if_valid(pass_word, get_stage,get_game):
    get_game.return_value = get_dummy_game()
    get_stage.return_value = get_dummy_stage()

    assert True is await pass_word_if_valid("no_important", 'test1')
    assert True is await pass_word_if_valid("no_important", 'test2')
    assert True is await pass_word_if_valid("no_important", 'test3')

    assert False is await pass_word_if_valid("no_important", 'test')
    assert False is await pass_word_if_valid("no_important", 'dummy')
    assert False is await pass_word_if_valid("no_important", 'another')


@pytest.mark.asyncio
async def test_pass_word(redis_with_stage):
    stage = await Stage.from_redis("test_stage")

    await stage.pass_word("NOT_IMPORTANT_HERE")
    assert 1 == stage.score

    await stage.pass_word("NOT_IMPORTANT_HERE")
    assert 2 == stage.score

    await stage.pass_word("NOT_IMPORTANT_HERE")
    assert 3 == stage.score
