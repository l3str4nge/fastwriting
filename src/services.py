from datetime import datetime

from .database.base import SessionLocal
from .database.operations import query_random_words
from .game.game import Game
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



async def create_level(session: SessionLocal, game_id: str, stage: int):
    redis = await get_redis()
    level_settings = STAGES[stage]
    level_data = {
        'stage': stage,
        'timeout': level_settings['timeout'],
        'words': query_random_words(session, level_settings['words_number'])
    }
    await redis.hmset(game_id, **level_data)
    return level_data


async def pass_word_if_valid(session: SessionLocal, game_id: str, word: str):
    redis = await get_redis()
    game = await redis.get_game(id=game_id)
    current_stage = game['current_stage']

    # stage = await redis.get_stage(game_id, stage=)

