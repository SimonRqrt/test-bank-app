import pytest
from mock_alchemy.mocking import UnifiedAlchemyMagicMock

@pytest.fixture(scope="function")
def session(engine, tables):
    # Créez une mock session utilisant UnifiedAlchemyMagicMock
    session = UnifiedAlchemyMagicMock()
    yield session
    session.rollback()

