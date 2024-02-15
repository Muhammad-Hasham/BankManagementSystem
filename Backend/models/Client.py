from pydantic import BaseModel
from models.Account import Account


class Client(BaseModel):
    firstname: str
    lastname: str
    email: str
    phoneNo: str
    NID: str
    address: str
    occupation: str
    sex: str
    birthdate: str
    account: Account