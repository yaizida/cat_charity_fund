from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, Extra


class CharityProjectBase(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = Field(None)
    full_amount: Optional[int] = Field(None)

    class Config:
        extra = Extra.forbid


class CharityProjectCreate(BaseModel):
    name: str = Field(..., max_length=100)
    description: str = Field(...)
    full_amount: int = Field(...)

    class Config:
        min_anystr_length = 1


class CharityProjectDB(CharityProjectCreate):
    id: int
    invested_amount: int = Field(0)
    fully_invested: bool = Field(False)
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True


class CharityProjectUpdate(CharityProjectBase):
    pass
