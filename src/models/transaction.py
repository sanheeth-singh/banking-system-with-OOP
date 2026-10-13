"""Transaction record model."""
from dataclasses import dataclass
from datetime import datetime
import uuid

@dataclass(frozen=True)
class Transaction:
    transaction_id: str
    timestamp: str
    transaction_type: str
    amount: float
    resulting_balance: float

    @classmethod
    def create(cls, tx_type: str, amount: float, resulting_balance: float):
        return cls(
            transaction_id=str(uuid.uuid4())[:8].upper(),
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            transaction_type=tx_type,
            amount=amount,
            resulting_balance=resulting_balance
        )