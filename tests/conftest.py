import pytest
import source.bank as bank
from mock_alchemy.mocking import UnifiedAlchemyMagicMock

@pytest.fixture(scope="function")
def session():
    # Créez une mock session utilisant UnifiedAlchemyMagicMock
    session = UnifiedAlchemyMagicMock()
    yield session
    session.rollback()

@pytest.fixture
def account_factory():
    def create_account(session, account_id, balance):
        return bank.Account(session=session, account_id=account_id, balance=balance)
    return create_account