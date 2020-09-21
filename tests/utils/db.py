from src.database.base import SessionLocal
from src.database.models import Dictionary


def fetch_all_polish_words(db: SessionLocal):
    return [str(raw.word) for raw in db.query(Dictionary).all()]
