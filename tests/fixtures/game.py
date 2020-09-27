import pytest

from src.game.game import Stage


@pytest.fixture
def stage():
    stage = Stage("TEST_STAGE")
    return stage