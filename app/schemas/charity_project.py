from datetime import datetime as dt
from typing import Optional

from pydantic import BaseModel, Extra, Field, PositiveInt


class CharityProjectBase(BaseModel):
    name: str = Field(None, min_length=1, max_length=100)
    description: str
    full_amount: PositiveInt

    class Config:
        extra = Extra.forbid


class CharityProjectCreate(CharityProjectBase):
    pass


class CharityProjectUpdate(CharityProjectBase):
    name: Optional[str]
    description: Optional[str]
    full_amount: Optional[PositiveInt]


class CharityProjectDB(CharityProjectBase):
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: dt
    close_date: Optional[dt]

    class Config:
        orm_mode = True
