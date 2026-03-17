# filepath: /d:/Others/Side Project/ipsystem/tests/conftest.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tests.tools.db_models import Base

# Create an in-memory SQLite database for testing
TEST_DATABASE_URL = "sqlite:///:memory:"

@pytest.fixture(scope='session')
def engine():
    return create_engine(TEST_DATABASE_URL)

@pytest.fixture(scope='session')
def tables(engine):
    # Create all tables
    Base.metadata.create_all(engine)
    yield
    # Drop all tables
    Base.metadata.drop_all(engine)

@pytest.fixture(scope='session')
def connection(engine, tables):
    connection = engine.connect()
    yield connection
    connection.close()

@pytest.fixture(scope='function')
def session(connection):
    # Create a new session for a test
    transaction = connection.begin()
    Session = sessionmaker(bind=connection)
    session = Session()

    yield session

    session.close()
    transaction.rollback()