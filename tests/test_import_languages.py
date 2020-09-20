from src.database.models import Language
from src.database.base import SessionLocal
from src.languages.importer import CSVWordsImporter
from tests.fixtures.dictionary import importer, importer_with_session
from tests.fixtures.db import db, session
from tests.utils.db import fetch_all_polish_words


def test_import_polish(importer: 'CSVWordsImporter'):
    words = importer.from_file('resources/polish.csv')

    assert len(words) == 2000
    assert words[1] == 'to'
    assert words[100] == 'właśnie'
    assert words[1000] == 'gotowa'
    assert words[1500] == 'pieprzyć'


def test_extract_word_from_row(importer: CSVWordsImporter):
    assert importer.extract_word(['1,2,3']) == '2'
    assert importer.extract_word(['1,test,3']) == 'test'
    assert importer.extract_word([]) == 'unknown'


def test_import_polish_to_db_without_exception(importer_with_session: CSVWordsImporter):
    importer_with_session.to_db()
    words = fetch_all_polish_words(importer_with_session.destination)

    assert len(words) == 2000
    assert str(words[0].word) == 'to'