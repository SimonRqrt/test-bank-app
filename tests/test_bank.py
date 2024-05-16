from source.bank import Account, Transaction
from datetime import datetime

def test_deposit_normal(session, account_factory):
    account = account_factory(account_id=1, balance=0.0)
    session.add(account)
    account.deposit(100.0)
    transaction = account.session.query(Transaction).first()
    assert account.balance == 100.0
    assert transaction.type == "deposit"
    assert isinstance(transaction.timestamp, datetime)
    assert account.session.commit.call_count == 1

def test_deposit_negative_amount(session, account_factory):
    account = account_factory(account_id=1, balance=80.0)
    session.add(account)
    account.deposit(-20.0)
    transaction = account.session.query(Transaction).all()
    assert account.balance == 80.0
    assert len(transaction) == 0
    assert account.session.commit.call_count == 0

def test_deposit_zero_amount(session, account_factory):
    account = account_factory(account_id=1, balance=70.0)
    session.add(account)
    account.deposit(0.0)
    transaction = account.session.query(Transaction).all()
    assert account.balance == 70.0
    assert len(transaction) == 0
    assert account.session.commit.call_count == 0


def test_withdraw_normal(session, account_factory):
    account = account_factory(account_id=1, balance=100.0)
    session.add(account)
    account.withdraw(50.0)
    transaction = account.session.query(Transaction).first()
    assert account.balance == 50.0
    assert transaction.type == "withdrawal"
    assert account.session.commit.call_count == 1

def test_withdraw_insufficient_funds():
    pass

def test_withdraw_negative_amount():
    pass

def test_withdraw_zero_amount():
    pass


def test_transfer_normal(session, account_factory):
    account1 = account_factory(account_id=1, balance=100.0)
    account2 = account_factory(account_id=2, balance=50.0)
    session.add(account1)
    session.add(account2)
    account1.transfer(account2, 50.0)
    assert account1.balance == 50.0
    assert account2.balance == 100.0

def test_transfer_insufficient_funds():
    pass

def test_transfer_negative_amount():
    pass

def test_transfer_zero_amount():
    pass


def test_get_balance_initial(session, account_factory):
    account = account_factory(account_id=1, balance=42.0)
    session.add(account)
    account.get_balance()
    assert account.balance == 42.0

def test_get_balance_after_deposit():
    pass

def test_get_balance_after_withdrawal():
    pass

def test_get_balance_after_failed_withdrawal():
    pass

def test_get_balance_after_transfer():
    pass

