from src.bank import Bank
from src.exceptions import BankingError

def display_menu():
    print("\n==================================")
    print("  bunnyMe9 OOP BANKING SYSTEM  ")
    print("===================================")
    print("1. Open Savings Account")
    print("2. Open Checking Account")
    print("3. Deposit Funds")
    print("4. Withdraw Funds")
    print("5. Transfer Funds")
    print("6. View Account Statement")
    print("7. Run Monthly Maintenance Cycle")
    print("8. List All Accounts")
    print("9. Exit")

def main():
    bank = Bank()

    while True:
        display_menu()
        choice = input("Select an option (1-9): ").strip()

        try:
            if choice == "1":
                name = input("Enter account holder name: ").strip()
                dep = float(input("Enter initial deposit ($100 min recommended): "))
                acc = bank.open_savings_account(name, dep)
                print(f"Savings Account created: {acc.account_number} | Balance: ${acc.balance:.2f}")

            elif choice == "2":
                name = input("Enter account holder name: ").strip()
                dep = float(input("Enter initial deposit: "))
                acc = bank.open_checking_account(name, dep)
                print(f"Checking Account created: {acc.account_number} | Balance: ${acc.balance:.2f}")

            elif choice == "3":
                acc_num = input("Enter account number: ").strip()
                amt = float(input("Enter deposit amount: "))
                acc = bank.get_account(acc_num)
                acc.deposit(amt)
                print(f"Deposit successful. New Balance: ${acc.balance:.2f}")

            elif choice == "4":
                acc_num = input("Enter account number: ").strip()
                amt = float(input("Enter withdrawal amount: "))
                acc = bank.get_account(acc_num)
                acc.withdraw(amt)
                print(f"Withdrawal complete. Remaining Balance: ${acc.balance:.2f}")

            elif choice == "5":
                src = input("Source account number: ").strip()
                dst = input("Destination account number: ").strip()
                amt = float(input("Transfer amount: "))
                bank.transfer(src, dst, amt)
                print(f"Transferred ${amt:.2f} from {src} to {dst}.")

            elif choice == "6":
                acc_num = input("Enter account number: ").strip()
                acc = bank.get_account(acc_num)
                print(f"\n--- Statement for {acc.account_holder} ({acc.account_number}) ---")
                print(f"Current Balance: ${acc.balance:.2f}\n")
                print(f"{'TX ID':<10} | {'Timestamp':<20} | {'Type':<18} | {'Amount':<10} | {'Resulting Bal'}")
                print("-" * 75)
                for tx in acc.get_statement():
                    print(f"{tx.transaction_id:<10} | {tx.timestamp:<20} | {tx.transaction_type:<18} | ${tx.amount:<9.2f} | ${tx.resulting_balance:.2f}")

            elif choice == "7":
                bank.process_all_monthly_cycles()
                print("Monthly interest applied to all active accounts.")

            elif choice == "8":
                print("\nRegistered Accounts:")
                for acc in bank.list_all_accounts():
                    acc_type = type(acc).__name__
                    print(f"• [{acc.account_number}] {acc.account_holder:<18} | Type: {acc_type:<15} | Balance: ${acc.balance:.2f}")

            elif choice == "9":
                print("Exiting application. Goodbye!")
                break
            else:
                print("Invalid input. Choose a number from 1 to 9.")

        except BankingError as be:
            print(f"[Banking Rule Violation] {be}")
        except ValueError:
            print("[Input Error] Numerical value expected. Please check your inputs.")
        except Exception as e:
            print(f"[System Error] {e}")

if __name__ == "__main__":
    main() 