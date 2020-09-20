import pytest
from alembic.command import upgrade
from alembic.config import Config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from settings.settings import DB_URL


@pytest.fixture(scope='module')
def db():
    engine = create_engine(DB_URL, echo=True)
    session_factory = sessionmaker(bind=engine)
    print('\n----- CREATE TEST DB CONNECTION POOL\n')

    _db = {
        'engine': engine,
        'session_factory': session_factory,
    }
    alembic_config = Config('alembic.ini')
    # alembic_config.set_main_option('sqlalchemy.url',)
    upgrade(alembic_config, 'head')
    print('\n----- RUN ALEMBIC MIGRATION\n')
    yield _db
    print('\n----- CREATE TEST DB INSTANCE POOL\n')

    engine.dispose()
    print('\n----- RELEASE TEST DB CONNECTION POOL\n')


@pytest.fixture(scope='module')
def session(db):
    session = db['session_factory']()
    yield session
    print('\n----- CREATE DB SESSION\n')

    session.rollback()
    session.close()
    print('\n----- ROLLBACK DB SESSION\n')