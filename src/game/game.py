from src.database.base import SessionLocal
from src.database.operations import query_random_words
from src.redis.interface import get_redis
from src.utils.date import now_to_str
from settings.stages import STAGES


class Game:
    INITIAL_STAGE = 1

    def __init__(self, username: str):
        self.username = username
        self.key = f"{hash(self.username)}_{self.username}"
        self.data = {
            'username': self.username,
            'started': "",
            'current_stage': self.INITIAL_STAGE
        }

    @classmethod
    async def create_for(cls, username: str) -> dict:
        instance = cls(username)
        instance.data['started'] = now_to_str()

        redis = await get_redis()
        await redis.hmset(instance.key, **instance.data)
        return instance.data

    @classmethod
    async def from_redis(cls, game_id: str):
        redis = await get_redis()
        game_data = await redis.hgetall(game_id)
        instance = cls(username=game_data['username'])
        instance.data['started'] = game_data['started']
        instance.data['current_stage'] = game_data['current_stage']
        return instance.data


class Stage:

    def __init__(self, game_id: str):
        self.game_id = game_id
        self.data = {
            "game_id": self.game_id,
            "number": "",
            "words": [],
            "timeout": ""
        }

    def generate_words(self, session: SessionLocal):
        self.data['words'] = query_random_words(session, self.stage_config['words_number'])

    @classmethod
    async def create(cls, session: SessionLocal,  game_id: str, number: int = 1):
        instance = cls(game_id, number)
        instance.generate_words(session)

        redis = await get_redis()
        await redis.hmset(instance.game_id, **instance.data)
        return instance.data

    @classmethod
    async def from_redis(cls, game_id: str):
        redis = await get_redis()
        game_data = await redis.hgetall(game_id)
        instance = cls(game_id=game_id, number=None)
        instance.data['started'] = game_data['started']
        instance.data['current_stage'] = game_data['current_stage']
        return instance.data
