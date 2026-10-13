"""Abstract base class establishing Account contract and encapsulation."""
from abc import ABC, abstractmethod
from typing import List, Dict
from src.models.transaction import Transaction
from src.exceptions import InvalidTransactionError

import os
import json

class Account(ABC):
    def __init__(self, account_number: str, account_holder: str, initial_deposit: float = 0.0, json_path: str = "data/bank_data.json"):
        if initial_deposit < 0:
            raise InvalidTransactionError("Initial deposit cannot be negative.")
        
        self._account_number = account_number
        self._account_holder = account_holder
        self._balance = float(initial_deposit)
        self.json_path = json_path
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

    def deposit(self, amount: float) -> bool:
        if amount <= 0:
            raise InvalidTransactionError("Deposit amount must be greater than zero.")
        
        self._balance += amount
        self._record_transaction("DEPOSIT", amount)
        return True

    @abstractmethod
    def withdraw(self, amount: float) -> bool:
        """Abstract method implemented polymorphically by child account types."""
        pass

    @abstractmethod
    def apply_monthly_process(self) -> None:
        """Abstract monthly calculation (e.g., interest accrual, maintenance fees)."""
        pass

    def _record_transaction(self, tx_type: str, amount: float) -> None:
        tx = Transaction.create(tx_type, amount, self._balance)
        self._transactions.append(tx)

    def get_statement(self) -> List[Transaction]:
        return list(self._transactions)