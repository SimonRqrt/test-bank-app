from source.bank import Account, Transaction
from datetime import datetime
import pytest

def test_deposit_normal(session, account_factory):
    account = account_factory(account_id=1, balance=0.0)
    session.add(account)
    account.deposit(100.0)
    transaction = account.session.query(Transaction).first()
    assert account.balance == 100.0
    assert transaction.type == "deposit"
    assert isinstance(transaction.timestamp, datetime)
    assert account.session.commit.call_count == 1

@pytest.mark.database
def test_deposit_negative_amount(session, account_factory):
    account = account_factory(account_id=1, balance=80.0)
    session.add(account)
    with pytest.raises(ValueError):
        account.deposit(-20.0)
    transaction = account.session.query(Transaction).all()
    assert account.balance == 80.0
    assert len(transaction) == 0
    assert account.session.commit.call_count == 0

@pytest.mark.database
def test_deposit_zero_amount(session, account_factory):
    account = account_factory(account_id=1, balance=70.0)
    session.add(account)
    with pytest.raises(ValueError):
        account.deposit(0.0)
    transaction = account.session.query(Transaction).all()
    assert account.balance == 70.0
    assert len(transaction) == 0
    assert account.session.commit.call_count == 0

@pytest.mark.database
def test_withdraw_normal(session, account_factory):
    account = account_factory(account_id=1, balance=100.0)
    session.add(account)
    account.withdraw(50.0)
    transaction = account.session.query(Transaction).first()
    assert account.balance == 50.0
    assert transaction.type == "withdrawal"
    assert account.session.commit.call_count == 1

@pytest.mark.database
def test_withdraw_insufficient_funds(session, account_factory):
    account = account_factory(account_id=1, balance=40.0)
    session.add(account)
    with pytest.raises(ValueError):
        account.withdraw(50.0)
    transaction = account.session.query(Transaction).all()
    assert account.balance == 40.0
    assert len(transaction) == 0
    assert account.session.commit.call_count == 0

@pytest.mark.database
def test_withdraw_negative_amount(session, account_factory):
    account = account_factory(account_id=1, balance=100)
    session.add(account)
    with pytest.raises(ValueError):
        account.withdraw(-100)
    transaction = account.session.query(Transaction).all()
    assert account.balance == 100
    assert len(transaction) == 0
    assert account.session.commit.call_count == 0

@pytest.mark.database
def test_withdraw_zero_amount(session, account_factory):
    account = account_factory(account_id=1, balance=100)
    session.add(account)
    with pytest.raises(ValueError):
        account.withdraw(0)
    transaction = account.session.query(Transaction).all()
    assert account.balance == 100
    assert len(transaction) == 0
    assert account.session.commit.call_count == 0

@pytest.mark.database
def test_transfer_normal(session, account_factory):
    account1 = account_factory(account_id=1, balance=100.0)
    account2 = account_factory(account_id=2, balance=50.0)
    session.add(account1)
    session.add(account2)
    account1.transfer(account2, 50.0)
    transaction1 = account1.session.query(Transaction).all()[0]
    transaction2 = account2.session.query(Transaction).all()[1]
    assert account1.balance == 50.0
    assert account2.balance == 100.0
    assert transaction1.type == "withdrawal"
    assert transaction2.type == "deposit"
    assert account1.session.commit.call_count == 2
    assert account2.session.commit.call_count == 2

@pytest.mark.database
def test_transfer_insufficient_funds():
    pass

@pytest.mark.database
def test_transfer_negative_amount():
    pass

@pytest.mark.database
def test_transfer_zero_amount():
    pass

@pytest.mark.database
def test_get_balance_initial(session, account_factory):
    account = account_factory(account_id=1, balance=42.0)
    session.add(account)
    account.get_balance()
    assert account.balance == 42.0

@pytest.mark.database
def test_get_balance_after_deposit(session, account_factory):
    account = account_factory(account_id=1, balance=0)
    session.add(account)
    account.deposit(100)
    assert account.get_balance() == 100


@pytest.mark.database
def test_get_balance_after_withdrawal(session, account_factory):
    account =account_factory(account_id=1, balance=200)
    session.add(account)
    account.withdraw(40)
    assert account.balance == 160

@pytest.mark.database
def test_get_balance_after_failed_withdrawal(session, account_factory):
    account =account_factory(account_id=1, balance=50)
    session.add(account)
    with pytest.raises(ValueError):
        account.withdraw(80)
    assert account.get_balance() == 50

@pytest.mark.database
def test_get_balance_after_transfer(session, account_factory):
    account =account_factory(account_id=1, balance=100)
    account2 =account_factory(account_id=2, balance=100)
    session.add(account)
    session.add(account2)
    account.transfer(account2,50)
    assert account.get_balance() == 50
    assert account2.get_balance() == 150



@pytest.mark.parametrize("initial_balance, deposit_amount, expected_balance", [
    (100, 50, 150),
    (200, 100, 300),
    (0, 100, 100),
])
def test_deposit(account_factory, initial_balance, deposit_amount, expected_balance):
    account = account_factory(account_id=1, balance=initial_balance)
    account.deposit(deposit_amount)
    assert account.balance == expected_balance

@pytest.mark.parametrize("initial_balance, withdraw_amount, expected_balance", [
    (100, 50, 50),
    (200, 100, 100),
    (100, 100, 0),
])
def test_withdraw(account_factory, initial_balance, withdraw_amount, expected_balance):
    account = account_factory(account_id=2, balance=initial_balance)
    account.withdraw(withdraw_amount)
    assert account.balance == expected_balance

@pytest.mark.parametrize("initial_balance, transfer_amount, expected_balance", [
    (100, 50, 50),
    (200, 100, 100),
    (100, 100, 0),
])
def test_transfer(account_factory, initial_balance, transfer_amount, expected_balance):
    account1 = account_factory(account_id=1, balance=initial_balance)
    account2 = account_factory(account_id=2, balance=0)
    account1.transfer(account2, transfer_amount)
    assert account1.balance == expected_balance
    assert account2.balance == transfer_amount