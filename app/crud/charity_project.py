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

    async def get_projects_by_completion_rate(self,
                                              session: AsyncSession):
        """Получает отсортированый список закрытых проектов."""
        projects = await session.execute(select(CharityProject).where(CharityProject.fully_invested))

        projects = projects.scalars().all()
        closed_projects = []
        for project in projects:
            closed_projects.append({'name': project.name,
                                    'description': project.description,
                                    'close_time': project.close_date - project.create_date,})
        return sorted(closed_projects, key=lambda time: time['close_time'])



project_crud = CRUDCharityProject(CharityProject)
