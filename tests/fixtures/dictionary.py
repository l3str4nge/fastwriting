import pytest

from src.languages.importer import CSVWordsImporter

from tests.fixtures.db import session, db

@pytest.fixture(scope='module')
def importer() -> CSVWordsImporter:
    return CSVWordsImporter()


@pytest.fixture(scope='module')
def importer_with_session(importer, session) -> CSVWordsImporter:
    importer.words = []
    importer.destination = session
    importer.from_file('resources/polish.csv')
    return importer