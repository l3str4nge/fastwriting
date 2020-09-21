import random

from .models import Dictionary
from .base import SessionLocal

def count_words(session: SessionLocal) -> int:
    return session.query(Dictionary.id).count()

def query_random_words(session: SessionLocal, how_many: int) -> list:
    limit = count_words(session)
    random_indexes = random.sample(range(1, limit), how_many)
    return session.query(Dictionary.word).filter(Dictionary.id.in_(random_indexes)).all()
