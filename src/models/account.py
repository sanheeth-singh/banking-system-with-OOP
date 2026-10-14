"""Abstract base class establishing Account contract and encapsulation."""
# src/models/account.py
from abc import ABC, abstractmethod
from typing import List
from src.models.transaction import Transaction
from src.exceptions import InvalidTransactionError

class Account(ABC):
    def __init__(self, account_number: str, account_holder: str, initial_deposit: float = 0.0):
        if initial_deposit < 0:
            raise InvalidTransactionError("Initial deposit cannot be negative.")
        
        self._account_number = account_number
        self._account_holder = account_holder
        self._balance = float(initial_deposit)
        self._transactions: List[Transaction] = []

        if initial_deposit > 0:
            self._record_transaction("INITIAL_DEPOSIT", initial_deposit)

    @property
    def account_number(self) -> str:
        return self._account_number

    @property
    def account_holder(self) -> str:
        return self._account_holder

    @property
    def balance(self) -> float:
        return self._balance

    def deposit(self, amount: float, note: str = "DEPOSIT") -> bool:
        if amount <= 0:
            raise InvalidTransactionError("Deposit amount must be greater than zero.")
        
        self._balance += amount
        self._record_transaction(note, amount)
        return True

    @abstractmethod
    def withdraw(self, amount: float, note: str = "WITHDRAWAL") -> bool:
        pass

    @abstractmethod
    def apply_monthly_process(self) -> None:
        pass

    def _record_transaction(self, tx_type: str, amount: float) -> None:
        tx = Transaction.create(tx_type, amount, self._balance)
        self._transactions.append(tx)

    def get_statement(self) -> List[Transaction]:
        return list(self._transactions)

    def to_dict(self) -> dict:
        return {
            "account_number": self._account_number,
            "account_holder": self._account_holder,
            "balance": round(self._balance, 2),
            "transactions": [tx.to_dict() for tx in self._transactions],
        }