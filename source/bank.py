from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Account(Base):
    __tablename__ = 'accounts'
    account_id = Column(Integer, primary_key=True)
    balance = Column(Float, default=0.0)
    transactions = relationship("Transaction", back_populates="account")

    def __init__(self, account_id, balance):
        self.account_id = account_id
        self.balance = balance

    def create_account(account_id, balance):
        account = Account(account_id=account_id, balance=balance)
        print("Account created")
        return account
    
    def create_transaction(self, amount, transaction_type):
        transaction = Transaction(amount=amount, type=transaction_type, timestamp=datetime.now(), account=self)
        return transaction

    def deposit(self, amount, session):
        self.balance += amount
        new_transaction = self.create_transaction(amount, "deposit")
        session.add(new_transaction)
        return self.balance

    def withdraw(self, amount, session):
        if self.balance >= amount:
            self.balance -= amount
            new_transaction = self.create_transaction(amount, "withdrawal")
            session.add(new_transaction)
            return self.balance
        else:
            return "Withdrawal not possible, not enough funds on balance"
        
    def transfer(self, other_account, amount, session):
        if self.balance >= amount:
            self.withdraw(amount, session)
            other_account.deposit(amount, session)
            return True
        else:
            return False

    def get_balance(self):
        return self.balance
           

class Transaction(Base):
    __tablename__ = 'transactions'
    transaction_id = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey('accounts.account_id'))
    amount = Column(Float)
    type = Column(String)
    timestamp = Column(DateTime)
    account = relationship("Account", back_populates="transactions")
