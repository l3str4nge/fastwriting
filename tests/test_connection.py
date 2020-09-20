from src.database.models import Language
from src.database.base import SessionLocal
from tests.fixtures import db, session


def test_language_exists(session):
    lang = session.query(Language).all()

    assert 1 == 2