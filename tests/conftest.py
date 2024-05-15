import pytest

import source.bank as bank

@pytest.fixture
def account_factory():
    def create_account(account_id, balance):
        return bank.Account(account_id=account_id, balance=balance)
    return create_account