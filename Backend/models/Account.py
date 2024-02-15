from models.Transaction import Transaction
from pydantic import BaseModel
from typing import List

class Account(BaseModel):
    accountNo: str = None  # Set to None as it will be generated
    pin: str
    balance: float
    transactions: List[Transaction] = []