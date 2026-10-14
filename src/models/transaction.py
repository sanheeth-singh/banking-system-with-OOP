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
            transaction_id=f"TX-{str(uuid.uuid4())[:8].upper()}",
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            transaction_type=tx_type,
            amount=round(amount, 2),
            resulting_balance=round(resulting_balance, 2)
        )

    def to_dict(self) -> dict:
        return {
            "transaction_id": self.transaction_id,
            "timestamp": self.timestamp,
            "transaction_type": self.transaction_type,
            "amount": self.amount,
            "resulting_balance": self.resulting_balance,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Transaction":
        return cls(
            transaction_id=data["transaction_id"],
            timestamp=data["timestamp"],
            transaction_type=data["transaction_type"],
            amount=data["amount"],
            resulting_balance=data["resulting_balance"]
        )