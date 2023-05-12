from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.services import investing
from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.donation import donation_crud
from app.models import User
from app.schemas.donation import DonationCreate, DonationDB, DonationGetAll

router = APIRouter()


@router.post('/',
             response_model=DonationDB,
             response_model_exclude_none=True)
async def create_donation(donation: DonationCreate,
                          session: AsyncSession = Depends(get_async_session),
                          user: User = Depends(current_user), ):
    """Сделать пожертвование."""
    donation = await donation_crud.create(donation,
                                          session,
                                          user)
    await investing(session)
    await session.refresh(donation)
    return donation


@router.get('/',
            response_model=List[DonationGetAll],
            response_model_exclude_none=True,
            dependencies=[Depends(current_superuser)])
async def get_all_donations(
        session: AsyncSession = Depends(get_async_session)):
    """
    Только для суперюзеров.

    Возвращает список всех пожертвований.
    """
    return await donation_crud.get_multi(session)


@router.get('/my',
            response_model=List[DonationDB])
async def get_user_donations(
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)):
    return await donation_crud.get_by_user(session=session,
                                           user=user)
