from datetime import datetime

from .database.base import SessionLocal
from .database.operations import query_random_words
from .game.game import Game, Stage
from .redis.interface import get_redis
from .utils.date import date_to_str, now_to_str
from settings.stages import STAGES
GameID = str


async def new_game(username: str) -> dict:
    """
    Game structure in redis:
    key: hash(username)_username
    fields:
        - started: time


    """
    return await Game.create_for(username)


async def create_stage(session: SessionLocal, game_id: str, stage: int):
    return await Stage.create(session, game_id, stage)


async def pass_word_if_valid(session: SessionLocal, game_id: str, word: str):
    redis = await get_redis()
    game = await redis.get_game(id=game_id)
    current_stage = game['current_stage']

    # stage = await redis.get_stage(game_id, stage=)

