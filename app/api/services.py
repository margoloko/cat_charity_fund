import copy
from datetime import datetime as dt
from http import HTTPStatus
from typing import Dict

#from aiogoogle import Aiogoogle
#from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


from app.core.config import settings
from app.models import CharityProject, Donation


async def investing(session: AsyncSession):
    donat = 0
    project = 0
    money = await session.execute(
        select(Donation).where(~Donation.fully_invested))
    money = money.scalars().all()

    prjcts = await session.execute(
        select(CharityProject).where(~CharityProject.fully_invested))
    prjcts = prjcts.scalars().all()
    while donat < len(money) and project < len(prjcts):
        balance = money[donat].full_amount - money[donat].invested_amount
        pr_bl = prjcts[project].full_amount - prjcts[project].invested_amount
        free_for_investing = min(balance, pr_bl)
        money[donat].invested_amount += free_for_investing
        prjcts[project].invested_amount += free_for_investing
        if money[donat].full_amount == money[donat].invested_amount:
            setattr(money[donat], 'fully_invested', True)
            setattr(money[donat], 'close_date', dt.now())
            donat += 1
        if prjcts[project].full_amount == prjcts[project].invested_amount:
            setattr(prjcts[project], 'fully_invested', True)
            setattr(prjcts[project], 'close_date', dt.now())
            project += 1
    session.add_all(money + prjcts)
    await session.commit()
