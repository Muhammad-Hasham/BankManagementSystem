import datetime
from pydantic import BaseModel
from typing import Optional
import random
import time

class Transaction(BaseModel):
    transactionId: Optional[str] = None  # Set to None as it will be generated
    fromAccount: str
    toAccount: str
    amount: str
    date: str
    transactionType: str

    @classmethod
    def create(cls, from_account: str, to_account: str, amount: float, transaction_type: str):
        return cls(
            transactionId=generate_transaction_id(),
            fromAccount=from_account,
            toAccount=to_account,
            amount=amount,
            date=datetime.datetime.now().isoformat(),
            transactionType=transaction_type
        )

def generate_transaction_id():
    timestamp = int(time.time())
    random_number = random.randint(100, 999)
    return f"{timestamp}{random_number}"
