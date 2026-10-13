"""Bank aggregate controller managing ledger and transfers."""
import random
from typing import Dict, List
from src.models.account import Account
from src.models.savings import SavingsAccount
from src.models.checking import CheckingAccount
from src.exceptions import AccountNotFoundError, InvalidTransactionError

class Bank():
    def __init__(self, name: str = "bunnyMe9 Federal Reserve"):
        self.name = name
        self._accounts: Dict[str, Account] = {}

    def _generate_account_number(self, prefix: str) -> str:
        while True:
            acc_num = f"{prefix}-{random.randint(100000, 999999)}"
            if acc_num not in self._accounts:
                return acc_num

    def open_savings_account(self, holder: str, initial_deposit: float) -> SavingsAccount:
        acc_num = self._generate_account_number("SAV")
        account = SavingsAccount(acc_num, holder, initial_deposit)
        self._accounts[acc_num] = account

        return account

    def open_checking_account(self, holder: str, initial_deposit: float) -> CheckingAccount:
        acc_num = self._generate_account_number("CHK")
        account = CheckingAccount(acc_num, holder, initial_deposit)
        self._accounts[acc_num] = account
        return account

    def get_account(self, account_number: str) -> Account:
        if account_number not in self._accounts:
            raise AccountNotFoundError(f"Account '{account_number}' not found.")
        return self._accounts[account_number]

    def transfer(self, source_acc_num: str, target_acc_num: str, amount: float) -> bool:
        if source_acc_num == target_acc_num:
            raise InvalidTransactionError("Cannot transfer funds to the exact same account.")
        
        source = self.get_account(source_acc_num)
        target = self.get_account(target_acc_num)

        # Atomic-style execution
        source.withdraw(amount)
        try:
            target.deposit(amount)
        except Exception as e:
            # Revert if target fails
            source.deposit(amount)
            raise e
        return True

    def process_all_monthly_cycles(self) -> None:
        for acc in self._accounts.values():
            acc.apply_monthly_process()

    def list_all_accounts(self) -> List[Account]:
        return list(self._accounts.values())