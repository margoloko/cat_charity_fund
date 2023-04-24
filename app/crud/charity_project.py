from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject


class CRUDCharityProject(CRUDBase):
    async def get_project_by_name(self,
                                  name: str,
                                  session: AsyncSession,
                                  ) -> Optional[int]:
        db_project_id = await session.execute(select(CharityProject.id).where(CharityProject.name == name))
        return db_project_id.scalars().first()


project_crud = CRUDCharityProject(CharityProject)
