from src.database.base import SessionLocal
from src.database.models import Dictionary


def fetch_all_polish_words(db: SessionLocal):
    return db.query(Dictionary).all()
