"""src/models/checking.py - Checking Account with overdraft support."""
from src.models.account import Account
from src.exceptions import InsufficientFundsError, InvalidTransactionError

class CheckingAccount(Account):
    def __init__(self, account_number: str, account_holder: str, initial_deposit: float = 0.0,
                 overdraft_limit: float = 500.0, overdraft_fee: float = 25.0):
        super().__init__(account_number, account_holder, initial_deposit)
        self._overdraft_limit = overdraft_limit
        self._overdraft_fee = overdraft_fee

    def withdraw(self, amount: float) -> bool:
        if amount <= 0:
            raise InvalidTransactionError("Withdrawal amount must be positive.")
        if (self._balance - amount) < -self._overdraft_limit:
            raise InsufficientFundsError(
                f"Withdrawal exceeds allowed overdraft limit of ${self._overdraft_limit:.2f}."
            )
        
        self._balance -= amount
        self._record_transaction("WITHDRAWAL", amount)
        
        # Apply overdraft penalty if balance dips negative
        if self._balance < 0:
            self._balance -= self._overdraft_fee
            self._record_transaction("OVERDRAFT_FEE", self._overdraft_fee)
            
        return True

    def apply_monthly_process(self) -> None:
        pass