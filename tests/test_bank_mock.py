from source.bank import Account, Transaction

def test_deposit_normal(session, account_factory):
    account = account_factory(session=session, account_id=1, balance=0.0)
    session.add(account)
    account.deposit(100.0)
    session.commit()
    assert account.balance == 100.0

def test_withdraw_normal(session, account_factory):
    account = account_factory(session=session, account_id=1, balance=100.0)
    session.add(account)
    account.withdraw(50.0)
    session.commit()
    assert account.balance == 50.0

def test_transfer_normal(session, account_factory):
    account1 = account_factory(session=session, account_id=1, balance=100.0)
    account2 = account_factory(session=session, account_id=2, balance=50.0)
    session.add(account1)
    session.add(account2)
    account1.transfer(account2, 50.0)
    assert account1.balance == 50.0
    assert account2.balance == 100.0

def test_get_balance_initial(session, account_factory):
    account = account_factory(session=session, account_id=1, balance=42.0)
    session.add(account)
    account.get_balance()
    assert account.balance == 42.0

