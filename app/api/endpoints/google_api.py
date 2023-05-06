from datetime import datetime
from typing import List

from aiogoogle import Aiogoogle
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.google_client import get_service
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.schemas.charity_project import CharityProjectDB
from app.services.google_api import (set_user_permissions,
                                     spreadsheets_create,
                                     spreadsheets_update_value)


router = APIRouter()

@router.get('/',
            response_model=List[CharityProjectDB],
            dependencies=[Depends(current_superuser)], )
async def get_report():
    pass
