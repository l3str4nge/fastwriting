import pytest

from src.languages.importer import WordsImporter

from tests.fixtures.db import session, db

@pytest.fixture(scope='module')
def importer() -> WordsImporter:
    return WordsImporter()


@pytest.fixture(scope='module')
def importer_with_session(importer, session) -> WordsImporter:
    importer.words = []
    importer.destination = session
    importer.from_file('resources/english.txt')
    return importer


@pytest.fixture(scope="module")
def session_with_words(importer_with_session: WordsImporter):
    importer_with_session.to_db()
    return importer_with_session.destination