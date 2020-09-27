from uuid import uuid1
from datetime import datetime, timedelta

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
            'started': datetime.now().strftime("%Y-%m-%d_%H:%S:%M"),
            'current_stage': self.INITIAL_STAGE
        }

    @property
    def current_stage(self):
        return self.data['current_stage']

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

    def __init__(self, stage_id: str, number: int = 1):
        self.stage_id = stage_id or str(uuid1())
        self.number = number
        self.data = {
            "game_id": "",
            "number": self.number,
            "words": [],
            "timeout": "",
            "started": "",
            "score": 0
        }

    @property
    def words(self) -> list:
        return self.data['words'].split(',')

    @property
    def score(self) -> int:
        return int(self.data['score'])

    @property
    def started(self) -> datetime:
        return datetime.strptime(self.data['started'], "%Y-%m-%d_%H:%M:%S")

    @property
    def timeout(self) -> int:
        return int(self.data['timeout'])

    def generate_words(self, session: SessionLocal):
        self.data['words'] = ','.join(query_random_words(session, STAGES[self.number]['words_number']))

    def set_timeout_from_settings(self):
        self.data['timeout'] = STAGES[self.number]['timeout']

    @classmethod
    async def create(cls, session: SessionLocal,  stage_id: str, number: int = 1):
        instance = cls(stage_id, number)
        instance.generate_words(session)
        instance.set_timeout_from_settings()
        redis = await get_redis()
        await redis.hmset(instance.stage_id, **instance.data)
        return instance.data

    @classmethod
    async def from_redis(cls, stage_id: str):
        redis = await get_redis()
        stage_data = await redis.hgetall(stage_id)
        instance = cls(stage_id=stage_id)
        instance.data['game_id'] = stage_data['game_id']
        instance.data['number'] = stage_data['number']
        instance.data['words'] = stage_data['words']
        instance.data['timeout'] = stage_data['timeout']
        instance.data['score'] = int(stage_data['score'])
        return instance

    async def pass_word(self, word: str):
        redis = await get_redis()
        result = await redis.hincrby(self.stage_id, "score", 1)
        self.data['score'] += 1
        return result

    async def check_timeout_expired(self) -> bool:
        return (datetime.now() - self.started).seconds > self.timeout


