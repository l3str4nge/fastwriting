import pytest
from tests.fixtures.db import session, db, session_with_words

from src.restapi import new_game


@pytest.mark.asyncio
@pytest.mark.freeze_time("2020-10-10 12:00:20")
async def test_new_game_endpoint(session_with_words):
    response = await new_game("TEST_USERNAME", session_with_words)

    assert response['game']
    assert response['game']['username'] == "TEST_USERNAME"
    assert response['game']['started'] == "2020-10-10_12:00:20"
    assert response['game']['current_stage'] == 1

    assert response['stage']
    assert response['stage']['number'] == 1
    assert response['stage']['timeout'] == 120
    assert response['stage']['score'] == 0
    assert len(response['stage']['words'].split(',')) == 60