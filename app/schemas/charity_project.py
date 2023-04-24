from datetime import datetime as dt
from typing import Optional

from pydantic import BaseModel, Extra, Field, PositiveInt


class CharityProjectBase(BaseModel):
    name: str = Field(..., max_length=100)
    description: str
    full_amount: PositiveInt

    class Config:
        min_anystr_length = 1


class CharityProjectCreate(CharityProjectBase):
    pass


class CharityProjectUpdate(CharityProjectBase):
    name: Optional[str]
    description: Optional[str]
    full_amount: Optional[PositiveInt]

    class Config:
        min_anystr_length = 1
        extra = Extra.forbid


class CharityProjectDB(CharityProjectBase):
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: dt
    close_date: Optional[dt]

    class Config:
        orm_mode = True
