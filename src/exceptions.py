"""Custom domain exceptions for the banking system."""

class BankingError(Exception):
    """Base exception for banking operations."""
    pass

class InsufficientFundsError(BankingError):
    """Raised when a withdrawal exceeds available balance and overdraft limits."""
    pass

class InvalidTransactionError(BankingError):
    """Raised when an illegal operation or invalid monetary value is supplied."""
    pass

class AccountNotFoundError(BankingError):
    """Raised when an account cannot be located in the ledger."""
    pass