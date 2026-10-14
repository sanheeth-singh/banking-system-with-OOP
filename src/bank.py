"""Bank aggregate controller managing ledger and transfers."""
import os
import json
import random
from typing import Dict, List
from src.models.account import Account
from src.models.savings import SavingsAccount
from src.models.checking import CheckingAccount
from src.models.transaction import Transaction
from src.exceptions import AccountNotFoundError, InvalidTransactionError

class Bank:
    def __init__(self, name: str = "Codomax Bank", data_file: str = "data/bank_data.json"):
        self.name = name
        self.data_file = data_file
        self._accounts: Dict[str, Account] = {}
        
        # Ensure directory exists and load persisted accounts
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        self.load_from_json()

    # --- File I/O Persistence ---
    def save_to_json(self) -> None:
        """Persists all accounts, balances, and transaction ledgers to disk."""
        data = {acc_num: acc.to_dict() for acc_num, acc in self._accounts.items()}
        try:
            with open(self.data_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
        except OSError as e:
            print(f"[Error saving bank data]: {e}")

    def load_from_json(self) -> None:
        """Reads bank_data.json and reconstructs active OOP account instances."""
        if not os.path.exists(self.data_file):
            return

        try:
            with open(self.data_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            for acc_num, info in data.items():
                acc_type = info.get("account_type")
                holder = info["account_holder"]
                balance = info["balance"]

                if acc_type == "SavingsAccount":
                    acc = SavingsAccount(
                        account_number=acc_num,
                        account_holder=holder,
                        initial_deposit=0.0,
                        interest_rate=info.get("interest_rate", 0.04),
                        minimum_balance=info.get("minimum_balance", 50.0)
                    )
                else:
                    acc = CheckingAccount(
                        account_number=acc_num,
                        account_holder=holder,
                        initial_deposit=0.0,
                        overdraft_limit=info.get("overdraft_limit", 500.0),
                        overdraft_fee=info.get("overdraft_fee", 25.0)
                    )

                # Restore balance and existing transaction history
                acc._balance = balance
                acc._transactions = [Transaction.from_dict(tx) for tx in info.get("transactions", [])]
                self._accounts[acc_num] = acc

        except (json.JSONDecodeError, OSError, KeyError) as e:
            print(f"[Warning]: Could not load data from {self.data_file} ({e}). Starting fresh.")

    # --- Account Factory & Operations ---
    def _generate_account_number(self, prefix: str) -> str:
        while True:
            num = f"{prefix}-{random.randint(100000, 999999)}"
            if num not in self._accounts:
                return num

    def open_savings_account(self, holder: str, initial_deposit: float) -> SavingsAccount:
        acc_num = self._generate_account_number("SAV")
        acc = SavingsAccount(acc_num, holder, initial_deposit)
        self._accounts[acc_num] = acc
        self.save_to_json()
        return acc

    def open_checking_account(self, holder: str, initial_deposit: float) -> CheckingAccount:
        acc_num = self._generate_account_number("CHK")
        acc = CheckingAccount(acc_num, holder, initial_deposit)
        self._accounts[acc_num] = acc
        self.save_to_json()
        return acc

    def get_account(self, account_number: str) -> Account:
        if account_number not in self._accounts:
            raise AccountNotFoundError(f"Account '{account_number}' not found.")
        return self._accounts[account_number]

    def deposit_to_account(self, account_number: str, amount: float) -> None:
        acc = self.get_account(account_number)
        acc.deposit(amount)
        self.save_to_json()

    def withdraw_from_account(self, account_number: str, amount: float) -> None:
        acc = self.get_account(account_number)
        acc.withdraw(amount)
        self.save_to_json()

    def transfer(self, source_acc_num: str, target_acc_num: str, amount: float) -> bool:
        """
        Executes a 2-party transfer:
        1. Validates inputs and existence of both accounts.
        2. Withdraws from Source (records TRANSFER_OUT).
        3. Deposits to Target (records TRANSFER_IN).
        4. Saves updated state to bank_data.json immediately.
        """
        if source_acc_num == target_acc_num:
            raise InvalidTransactionError("Cannot transfer funds to the same account.")
        
        source = self.get_account(source_acc_num)
        target = self.get_account(target_acc_num)

        # Atomic transaction logic
        source.withdraw(amount, note=f"TRANSFER_OUT (to {target_acc_num})")
        try:
            target.deposit(amount, note=f"TRANSFER_IN (from {source_acc_num})")
        except Exception as e:
            # Rollback if deposit fails unexpectedly
            source.deposit(amount, note="TRANSFER_REVERSAL")
            self.save_to_json()
            raise e

        # Persist both updated accounts to bank_data.json
        self.save_to_json()
        return True

    def process_all_monthly_cycles(self) -> None:
        for acc in self._accounts.values():
            acc.apply_monthly_process()
        self.save_to_json()

    def list_all_accounts(self) -> List[Account]:
        return list(self._accounts.values())