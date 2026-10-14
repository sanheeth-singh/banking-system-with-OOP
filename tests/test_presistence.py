from src.bank import Bank

def run_test():
    bank = Bank()

    # 1. Create User A and User B
    acc_a = bank.open_savings_account("User A", 100.0)
    acc_b = bank.open_checking_account("User B", 50.0)
    print(f"Initial: {acc_a.account_holder} = ${acc_a.balance}, {acc_b.account_holder} = ${acc_b.balance}")

    # 2. Transfer $40 from User A to User B
    print("\nExecuting transfer of $40...")
    bank.transfer(acc_a.account_number, acc_b.account_number, 40.0)

    # 3. Simulate restarting the bank system (reloads from bank_data.json)
    reloaded_bank = Bank()
    reloaded_a = reloaded_bank.get_account(acc_a.account_number)
    reloaded_b = reloaded_bank.get_account(acc_b.account_number)

    print(f"\nAfter Reload from JSON:")
    print(f"{reloaded_a.account_holder} Balance: ${reloaded_a.balance:.2f} (Expected: $60.00)")
    print(f"{reloaded_b.account_holder} Balance: ${reloaded_b.balance:.2f} (Expected: $90.00)")
    print(f"{reloaded_a.account_holder} Last Tx: {reloaded_a.get_statement()[-1].transaction_type}")
    print(f"{reloaded_b.account_holder} Last Tx: {reloaded_b.get_statement()[-1].transaction_type}")

if __name__ == "__main__":
    run_test()