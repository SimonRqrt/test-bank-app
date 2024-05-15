from source.bank import Account, Transaction

def test_deposit(session):
    account = Account(account_id=1, balance=0.0)
    account.deposit(100.0, session)
    assert account.balance == 100.0

def test_withdraw(session):
    account = Account(account_id=1, balance=100.0)
    account.withdraw(50.0, session)
    assert account.balance == 50.0

def test_transfer(session):
    account1 = Account(account_id=1, balance=100.0)
    account2 = Account(account_id=2, balance=50.0)
    account1.transfer(account2, 30.0, session)
    assert account1.balance == 70.0
    assert account2.balance == 80.0