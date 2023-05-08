from typing import Dict, List, Optional

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
                                              session: AsyncSession
                                              ) -> Optional[List[Dict[str, str]]]:
        """Получает отсортированый список закрытых проектов."""
        projects = await session.execute(select(CharityProject).where(CharityProject.fully_invested == 1))
        projects = projects.scalars().all()
        closed_projects = []
        for project in projects:
            closed_projects.append({'name': project.name,
                                    'close_time': project.close_date - project.create_date,
                                    'description': project.description, })
        return sorted(closed_projects, key=lambda t: t['close_time'])


project_crud = CRUDCharityProject(CharityProject)
