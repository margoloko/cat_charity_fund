from datetime import datetime as dt
from typing import Optional

from pydantic import BaseModel, PositiveInt


class DonationBase(BaseModel):
    full_amount: PositiveInt
    comment: Optional[str]


class DonationCreate(DonationBase):
    pass


class DonationDB(DonationBase):
    id: int
    create_date: dt

    class Config:
        orm_mode = True


class DonationGetAll(DonationDB):
    user_id: int
    invested_amount: int
    fully_invested: bool
    close_date: Optional[dt]
