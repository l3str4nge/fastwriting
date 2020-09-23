from src.redis.interface import get_redis
from src.utils.date import now_to_str


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
