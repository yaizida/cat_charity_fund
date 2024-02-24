from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, Extra, PositiveInt

DEFAULT_INVESTED_AMOUNT = 0
DEFAULT_FULLY_INVESTED = False


class CharityProjectBase(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = Field(None)
    full_amount: Optional[PositiveInt] = Field(None)

    class Config:
        extra = Extra.forbid
        min_anystr_length = 1


class CharityProjectCreate(BaseModel):
    name: str = Field(..., max_length=100)
    description: str = Field(...)
    full_amount: PositiveInt = Field(...)

    class Config:
        min_anystr_length = 1


class CharityProjectDB(CharityProjectCreate):
    id: int
    invested_amount: int = Field(DEFAULT_INVESTED_AMOUNT)
    fully_invested: bool = Field(DEFAULT_FULLY_INVESTED)
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True


class CharityProjectUpdate(CharityProjectBase):
    pass
