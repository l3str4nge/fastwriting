from datetime import datetime

from .database.base import SessionLocal
from .database.operations import query_random_words
from .redis.interface import get_redis
from .utils.date import date_to_str, now_to_str
from settings.stages import STAGES
GameID = str

async def new_game_in_redis(username: str) -> GameID:
    """
    Game structure in redis:
    key: hash(username)_username
    fields:
        - started: time


    """
    redis = await get_redis()
    key = f"{hash(username)}_{username}"
    game_data = {
        'started': now_to_str()
    }
    await redis.hmset_dict(key, **game_data)
    return key


async def create_level(session: SessionLocal, game_id: str, stage: int):
    redis = await get_redis()
    level_settings = STAGES[stage]
    level_data = {
        'stage': stage,
        'timeout': level_settings['timeout'],
        'words': query_random_words(session, level_settings['words_number'])
    }
    await redis.hmset_dict(game_id, level_data)
    return level_data



