from pydantic import BaseModel
from typing import Optional


class ReceiverBase(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None


class ReceiverCreate(ReceiverBase):
    pass


class ReceiverUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None


class ReceiverInDBBase(ReceiverBase):
    id: int

    class Config:
        orm_mode = True


class Receiver(ReceiverInDBBase):
    pass
