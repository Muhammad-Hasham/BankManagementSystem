from pydantic import BaseModel
from fastapi import APIRouter, HTTPException
from pymongo import MongoClient
import random
import time
from models.Transaction import Transaction
from models.Client import Client


router = APIRouter()
client = MongoClient("mongodb://localhost:27017/BMS")
db = client.BMS


class LoginCredentials(BaseModel):
    accountNo: str
    pin: str

class TransferRequest(BaseModel):
    fromAccount: str
    toAccount: str
    amount: float
    pin: str  

class UpdatePin(BaseModel):
    oldPin: str
    newPin: str

class UpdateEmail(BaseModel):
    newEmail: str

class UpdatePhone(BaseModel):
    newPhoneNo: str

class UpdateAddress(BaseModel):
    newAddress: str

class UpdateOccupation(BaseModel):
    newOccupation: str

class BillPayment(BaseModel):
    billId: str
    billType: str
    amount: float
    pin: str
    



def generate_account_number():
    timestamp = int(time.time())
    random_number = random.randint(100, 999)
    return f"{timestamp}{random_number}"


@router.post("/signup")
async def signup(client: Client):
    try:
        client.account.accountNo = generate_account_number()
        
        # Insert the client into the database
        db.clients.insert_one(client.dict())
        return {"status": "success", "accountNo": client.account.accountNo}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.post("/login")
async def login(credentials: LoginCredentials):
    try:
        # Check if account exists
        client = db.clients.find_one({"account.accountNo": credentials.accountNo})
        if client is None:
            raise Exception("Account does not exist")
        
        # Check if pin matches
        if client["account"]["pin"] != credentials.pin:
            raise Exception("Incorrect pin")
        
        # Convert ObjectId to string
        client["_id"] = str(client["_id"])
        
        return {"status": "success", "data": client}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    
@router.get("/balance/{accountNo}")
async def get_account_balance(accountNo: str):
    try:
        # Retrieve the client with the given account number
        client = db.clients.find_one({"account.accountNo": accountNo})

        if client is None:
            raise HTTPException(status_code=404, detail="Account not found")

        # Extract the balance from the client's account
        balance = client["account"]["balance"]
        return {"accountNo": accountNo, "balance": balance}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/transfer")
async def transfer_funds(transfer_request: TransferRequest):
    try:
        # Fetch source and destination accounts
        source_client = db.clients.find_one({"account.accountNo": transfer_request.fromAccount})
        destination_client = db.clients.find_one({"account.accountNo": transfer_request.toAccount})

        if not source_client:
            raise HTTPException(status_code=404, detail="Source account not found")
        if not destination_client:
            raise HTTPException(status_code=404, detail="Destination account not found")
        if source_client["account"]["pin"] != transfer_request.pin:
            raise HTTPException(status_code=403, detail="Invalid PIN")
        if source_client["account"]["balance"] < transfer_request.amount:
            raise HTTPException(status_code=400, detail="Insufficient funds")

        # Perform the transfer
        new_source_balance = source_client["account"]["balance"] - transfer_request.amount
        new_destination_balance = destination_client["account"]["balance"] + transfer_request.amount

        # Create transaction records
        source_transaction = Transaction.create(
            from_account=transfer_request.fromAccount,
            to_account=transfer_request.toAccount,
            amount=f"-Rs{transfer_request.amount}",
            transaction_type="Fund Transfer"
        )
        destination_transaction = Transaction.create(
            from_account=transfer_request.fromAccount,
            to_account=transfer_request.toAccount,
            amount= f"+Rs{transfer_request.amount}",
            transaction_type="Fund Transfer"
        )

        # Update source and destination accounts
        db.clients.update_one(
            {"account.accountNo": transfer_request.fromAccount},
            {"$set": {"account.balance": new_source_balance}, "$push": {"account.transactions": source_transaction.dict()}}
        )
        db.clients.update_one(
            {"account.accountNo": transfer_request.toAccount},
            {"$set": {"account.balance": new_destination_balance}, "$push": {"account.transactions": destination_transaction.dict()}}
        )

        return {"status": "success", "message": "Transfer completed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.put("/updatePin/{accountNo}")
async def update_pin(accountNo: str, update_pin: UpdatePin):
    try:
        # Fetch the client
        client = db.clients.find_one({"account.accountNo": accountNo})
        if client is None:
            raise HTTPException(status_code=404, detail="Account not found")
        
        # Check if the old PIN matches
        if client["account"]["pin"] != update_pin.oldPin:
            raise HTTPException(status_code=403, detail="Invalid PIN")
        
        # Update the PIN
        db.clients.update_one(
            {"account.accountNo": accountNo},
            {"$set": {"account.pin": update_pin.newPin}}
        )
        return {"status": "success", "message": "PIN updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/transactions/{accountNo}")
async def get_transactions(accountNo: str):
    try:
        # Fetch the client
        client = db.clients.find_one({"account.accountNo": accountNo})
        if client is None:
            raise HTTPException(status_code=404, detail="Account not found")
        
        # Extract the transactions
        transactions = client["account"]["transactions"]
        return {"status": "success", "transactions": transactions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#update client's email
@router.put("/updateEmail/{accountNo}")
async def update_email(accountNo: str, update_email: UpdateEmail):
    try:
        # Fetch the client
        client = db.clients.find_one({"account.accountNo": accountNo})
        if client is None:
            raise HTTPException(status_code=404, detail="Account not found")
        
        # Update the email
        db.clients.update_one(
            {"account.accountNo": accountNo},
            {"$set": {"email": update_email.newEmail}}
        )
        return {"status": "success", "message": "Email updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#update client's phone number
@router.put("/updatePhone/{accountNo}")
async def update_phone(accountNo: str, update_phone: UpdatePhone):
    try:
        # Fetch the client
        client = db.clients.find_one({"account.accountNo": accountNo})
        if client is None:
            raise HTTPException(status_code=404, detail="Account not found")
        
        # Update the phone number
        db.clients.update_one(
            {"account.accountNo": accountNo},
            {"$set": {"phoneNo": update_phone.newPhoneNo}}
        )
        return {"status": "success", "message": "Phone number updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

#update client's address
@router.put("/updateAddress/{accountNo}")
async def update_address(accountNo: str, update_address: UpdateAddress):
    try:
        # Fetch the client
        client = db.clients.find_one({"account.accountNo": accountNo})
        if client is None:
            raise HTTPException(status_code=404, detail="Account not found")
        
        # Update the address
        db.clients.update_one(
            {"account.accountNo": accountNo},
            {"$set": {"address": update_address.newAddress}}
        )
        return {"status": "success", "message": "Address updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#update client's occupation
@router.put("/updateOccupation/{accountNo}")
async def update_occupation(accountNo: str, update_occupation: UpdateOccupation):
    try:
        # Fetch the client
        client = db.clients.find_one({"account.accountNo": accountNo})
        if client is None:
            raise HTTPException(status_code=404, detail="Account not found")
        
        # Update the occupation
        db.clients.update_one(
            {"account.accountNo": accountNo},
            {"$set": {"occupation": update_occupation.newOccupation}}
        )
        return {"status": "success", "message": "Occupation updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.post("/billPayment/{accountNo}")
async def bill_payment(accountNo: str, bill_payment: BillPayment):
    try:
        # Fetch the client
        client = db.clients.find_one({"account.accountNo": accountNo})
        if client is None:
            raise HTTPException(status_code=404, detail="Account not found")
        
        # Check if the PIN matches
        if client["account"]["pin"] != bill_payment.pin:
            raise HTTPException(status_code=403, detail="Invalid PIN")
        
        # Update the balance
        new_balance = client["account"]["balance"] - bill_payment.amount
        db.clients.update_one(
            {"account.accountNo": accountNo},
            {"$set": {"account.balance": new_balance}}
        )
        
        # Create transaction record
        transaction = Transaction.create(
            from_account=accountNo,
            to_account=bill_payment.billId,
            amount=f"-Rs{bill_payment.amount}",
            transaction_type=f"{bill_payment.billType} Bill Payment"
        )
        
        # Update the transactions
        db.clients.update_one(
            {"account.accountNo": accountNo},
            {"$push": {"account.transactions": transaction.dict()}}
        )
        
        return {"status": "success", "message": "Bill paid successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))