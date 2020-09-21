from src.database.models import Language
from src.database.base import SessionLocal
from src.database.operations import query_random_words
from src.languages.importer import WordsImporter
from tests.fixtures.dictionary import importer, importer_with_session, session_with_words
from tests.fixtures.db import db, session
from tests.utils.db import fetch_all_polish_words


def test_query_random_words(session_with_words):
    assert len(query_random_words(session_with_words, 20)) == 20
    assert len(query_random_words(session_with_words, 2)) == 2
    assert len(query_random_words(session_with_words, 400)) == 400
