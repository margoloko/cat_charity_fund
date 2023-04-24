from typing import List, Union
from datetime import datetime as dt

from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.charity_project import CharityProjectDB
from app.schemas.donation import DonationDB


async def investing(
    new_object: Union[CharityProjectDB, DonationDB],
    list_to_invest: List[Union[CharityProjectDB, DonationDB]],
    session: AsyncSession,
) -> Union[CharityProjectDB, DonationDB]:
    for obj_to_invest in list_to_invest:
        need_amount = obj_to_invest.full_amount - obj_to_invest.invested_amount
        if new_object.full_amount > need_amount:
            new_object.invested_amount = new_object.invested_amount + need_amount
            obj_to_invest.invested_amount = obj_to_invest.full_amount
        elif new_object.full_amount < need_amount:
            obj_to_invest.invested_amount = obj_to_invest.invested_amount + new_object.full_amount
            new_object.invested_amount = new_object.full_amount
        elif new_object.full_amount == need_amount:
            new_object.invested_amount = new_object.full_amount
            obj_to_invest.invested_amount = obj_to_invest.full_amount

        if new_object.invested_amount == new_object.full_amount:
            new_object.fully_invested = True
            new_object.close_date = dt.now()
        if obj_to_invest.invested_amount == obj_to_invest.full_amount:
            obj_to_invest.fully_invested = True
            obj_to_invest.close_date = dt.now()
        session.add(obj_to_invest)
        session.add(new_object)
        if new_object.fully_invested:
            break
    await session.commit()
    await session.refresh(new_object)
    return new_object
