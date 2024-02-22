from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class DonationBase(BaseModel):
    full_ammount: int
    comment: Optional[str]


class DonationCreate(DonationBase):
    id: int
    create_date: datetime


class DonationDB(DonationCreate):
    id: int
    create_date: datetime
    user_id: int
    invested_amount: int = Field(0)
    fully_invested: bool
    close_date: Optional[datetime]

    class Config:
        orm_mpde = True
