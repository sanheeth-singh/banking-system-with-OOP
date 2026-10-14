# src/models/savings.py
from src.models.account import Account
from src.exceptions import InsufficientFundsError, InvalidTransactionError

class SavingsAccount(Account):
    def __init__(self, account_number: str, account_holder: str, initial_deposit: float = 100.0,
                 interest_rate: float = 0.04, minimum_balance: float = 50.0):
        super().__init__(account_number, account_holder, initial_deposit)
        self._interest_rate = interest_rate
        self._minimum_balance = minimum_balance

    def withdraw(self, amount: float, note: str = "WITHDRAWAL") -> bool:
        if amount <= 0:
            raise InvalidTransactionError("Withdrawal amount must be strictly positive.")
        if (self._balance - amount) < self._minimum_balance:
            raise InsufficientFundsError(
                f"Withdrawal denied. Minimum balance required is ${self._minimum_balance:.2f}."
            )
        
        self._balance -= amount
        self._record_transaction(note, amount)
        return True

    def apply_monthly_process(self) -> None:
        monthly_interest = self._balance * (self._interest_rate / 12)
        if monthly_interest > 0:
            self._balance += monthly_interest
            self._record_transaction("INTEREST_CREDIT", round(monthly_interest, 2))

    def to_dict(self) -> dict:
        data = super().to_dict()
        data.update({
            "account_type": "SavingsAccount",
            "interest_rate": self._interest_rate,
            "minimum_balance": self._minimum_balance
        })
        return data