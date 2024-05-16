import pytest
from source.bank import Base, Account
from mock_alchemy.mocking import UnifiedAlchemyMagicMock
from sqlalchemy import create_engine

@pytest.fixture(scope="session")
def engine():
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def session(engine):
    # Créez une mock session utilisant UnifiedAlchemyMagicMock
    session = UnifiedAlchemyMagicMock(bind=engine)
    yield session
    session.rollback()

@pytest.fixture
def account_factory(session):
    def create_account(account_id, balance):
        return Account(session=session, account_id=account_id, balance=balance)
    return create_account
